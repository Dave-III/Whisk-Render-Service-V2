import asyncio
import json
import os
import re
import shutil
import threading
from collections import deque
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from .services.cleanup.cleanup import cleanup_old_files, write_job_manifest
from .services.media.resolver import resolve_media_input
from .services.render_status import (
    finish_render,
    get_render_status,
    reset_render_status,
    set_finalize_stage,
    set_render_error,
    set_render_stage,
    set_sync_stage,
    start_render,
)
from .services.rendering.renderer import render_side_by_side
from .services.storage.paths import ACTIVE_JOB_IDS, JOBS_DIR
from .services.youtube.uploader import upload_video


JANITOR_INTERVAL_SECONDS = 15 * 60
JOB_ID_PATTERN = re.compile(r"^[a-f0-9]{32}$")
OUTPUT_NAME_PATTERN = re.compile(r"^[A-Za-z0-9_-][A-Za-z0-9_.-]{0,99}\.mp4$")
QUEUE_LOCK = threading.Lock()
RENDER_QUEUE: deque[dict] = deque()
QUEUE_WORKER_SCHEDULED = False
ACTIVE_RENDER_JOB_ID: str | None = None


async def cleanup_loop() -> None:
    while True:
        await asyncio.sleep(JANITOR_INTERVAL_SECONDS)
        try:
            await asyncio.to_thread(cleanup_old_files)
        except Exception:
            print("Whisk cleanup pass failed")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.to_thread(cleanup_old_files)
    janitor = asyncio.create_task(cleanup_loop())
    try:
        yield
    finally:
        janitor.cancel()
        try:
            await janitor
        except asyncio.CancelledError:
            pass


app = FastAPI(title="Whisk Render Service", version="2.0", lifespan=lifespan)
allowed_origins = [
    origin.strip()
    for origin in os.getenv("WHISK_ALLOWED_ORIGINS", "*").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_output_stem(value: str) -> str:
    requested = Path(value or "whisk-render").name
    stem = requested[:-4] if requested.lower().endswith(".mp4") else requested
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", stem).strip("_-.")[:100]
    return cleaned or "whisk-render"


def safe_output_filename(value: str, job_id: str) -> str:
    return f"{safe_output_stem(value)[:80]}_{job_id[:8]}.mp4"


def safe_download_filename(value: str) -> str:
    return f"{safe_output_stem(value)}.mp4"


def process_render(job_id: str, job_dir: Path, clip1_path: Path, clip2_path: Path, auto_sync: bool, output_name: str) -> None:
    try:
        write_job_manifest(job_dir, state="processing", updated_at=utc_now())
        start_render(job_id)
        if auto_sync:
            set_sync_stage(job_id)

        set_render_stage(job_id)
        output_path = render_side_by_side(
            clip1_path,
            clip2_path,
            output_name=output_name,
            output_dir=job_dir / "output",
            enable_auto_sync=auto_sync,
        )

        set_finalize_stage(job_id)
        finish_render(job_id, f"/download/{job_id}", output_path.name)
        write_job_manifest(
            job_dir,
            state="complete",
            updated_at=utc_now(),
            output={
                "filename": output_path.name,
                "download_filename": safe_download_filename(output_name),
                "media_type": "video/mp4",
            },
        )
    except Exception as error:
        message = str(error).strip() or "The render failed. Try another pair of clips."
        set_render_error(job_id, message[:1200])
        write_job_manifest(job_dir, state="failed", updated_at=utc_now(), error=message[:1200])
    finally:
        ACTIVE_JOB_IDS.discard(job_id)


def process_render_queue() -> None:
    global ACTIVE_RENDER_JOB_ID, QUEUE_WORKER_SCHEDULED
    while True:
        with QUEUE_LOCK:
            if not RENDER_QUEUE:
                ACTIVE_RENDER_JOB_ID = None
                QUEUE_WORKER_SCHEDULED = False
                return
            job = RENDER_QUEUE.popleft()
            ACTIVE_RENDER_JOB_ID = job["job_id"]

        process_render(**job)

        with QUEUE_LOCK:
            ACTIVE_RENDER_JOB_ID = None


@app.get("/")
def root():
    return {"status": "running", "service": "Whisk Render Service", "version": "2.0"}


@app.get("/health")
def health_check():
    return {"healthy": True}


@app.get("/render-status")
def render_status_route(job_id: str | None = None):
    status = get_render_status(job_id)
    if status.get("state") == "queued":
        with QUEUE_LOCK:
            queue_position = next(
                (index + 1 for index, job in enumerate(RENDER_QUEUE) if job["job_id"] == status["job_id"]),
                None,
            )
            status["queue_position"] = queue_position
            if queue_position is not None:
                status["stage"] = f"Queued - position {queue_position}"
    else:
        status["queue_position"] = None
    return status


@app.post("/render")
def render(
    background_tasks: BackgroundTasks,
    clip1: UploadFile | None = File(None),
    clip2: UploadFile | None = File(None),
    clip1_url: str | None = Form(None),
    clip2_url: str | None = Form(None),
    auto_sync: bool = Form(True),
    output_name: str = Form("whisk-render"),
):
    job_id = uuid4().hex
    job_dir = JOBS_DIR / job_id
    inputs_dir = job_dir / "inputs"
    try:
        (job_dir / "output").mkdir(parents=True, exist_ok=False)
        inputs_dir.mkdir()
        ACTIVE_JOB_IDS.add(job_id)
        reset_render_status(job_id)

        clip1_path = resolve_media_input(clip1, clip1_url, inputs_dir)
        clip2_path = resolve_media_input(clip2, clip2_url, inputs_dir)
        output_filename = safe_output_filename(output_name, job_id)
        download_filename = safe_download_filename(output_name)
        write_job_manifest(
            job_dir,
            schema_version=1,
            job_id=job_id,
            state="queued",
            created_at=utc_now(),
            updated_at=utc_now(),
            inputs={"clip1": f"inputs/{clip1_path.name}", "clip2": f"inputs/{clip2_path.name}"},
            output={
                "filename": output_filename,
                "download_filename": download_filename,
                "media_type": "video/mp4",
            },
        )
        job = {
            "job_id": job_id,
            "job_dir": job_dir,
            "clip1_path": clip1_path,
            "clip2_path": clip2_path,
            "auto_sync": auto_sync,
            "output_name": output_filename,
        }
        with QUEUE_LOCK:
            RENDER_QUEUE.append(job)
            queue_position = len(RENDER_QUEUE) if ACTIVE_RENDER_JOB_ID is not None else len(RENDER_QUEUE)
            should_start_worker = not QUEUE_WORKER_SCHEDULED
            if should_start_worker:
                QUEUE_WORKER_SCHEDULED = True
        if should_start_worker:
            background_tasks.add_task(process_render_queue)
    except Exception as error:
        ACTIVE_JOB_IDS.discard(job_id)
        shutil.rmtree(job_dir, ignore_errors=True)
        if isinstance(error, HTTPException):
            raise
        if isinstance(error, (ValueError, RuntimeError)):
            raise HTTPException(status_code=422, detail=str(error)) from error
        raise HTTPException(status_code=502, detail="Unable to prepare the uploaded clips") from error

    return {"success": True, "job_id": job_id, "queue_position": queue_position}


@app.get("/download/{job_id}")
def download_video(job_id: str):
    if not JOB_ID_PATTERN.fullmatch(job_id):
        raise HTTPException(status_code=404, detail="Render not found")

    job_dir = JOBS_DIR / job_id
    manifest_path = job_dir / "manifest.json"
    if not manifest_path.is_file():
        raise HTTPException(status_code=404, detail="Render not found")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        filename = manifest["output"]["filename"]
        download_filename = manifest["output"].get("download_filename", filename)
        if manifest.get("state") != "complete":
            raise HTTPException(status_code=404, detail="Render output not ready")
    except (OSError, KeyError, TypeError, ValueError):
        raise HTTPException(status_code=404, detail="Render output not found")

    if not OUTPUT_NAME_PATTERN.fullmatch(filename):
        raise HTTPException(status_code=404, detail="Render output not found")
    file_path = job_dir / "output" / filename
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Render output not found")

    if not OUTPUT_NAME_PATTERN.fullmatch(download_filename):
        download_filename = filename

    return FileResponse(file_path, media_type="video/mp4", filename=download_filename)


@app.post("/upload-youtube")
def upload_to_youtube(filename: str = Form(...), title: str = Form(...)):
    if not OUTPUT_NAME_PATTERN.fullmatch(filename):
        raise HTTPException(status_code=404, detail="Rendered file not found")

    file_path = next(JOBS_DIR.glob(f"*/output/{filename}"), None)
    if file_path is None or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Rendered file not found")

    try:
        youtube_url = upload_video(file_path, title)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=502, detail="YouTube upload failed") from error

    return {"youtube_url": youtube_url}
