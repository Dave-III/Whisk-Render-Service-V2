from fastapi import FastAPI, UploadFile, BackgroundTasks, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from app.services.cleanup.cleanup import (
    cleanup_old_files
)
from app.services.media.resolver import (
    resolve_media_input
)
from app.services.youtube.uploader import upload_video
from app.services.rendering.renderer import (
    render_side_by_side,
    OUTPUT_DIR
)
from app.services.render_status import (
    start_render,
    set_sync_stage,
    set_render_stage,
    set_finalize_stage,
    finish_render,
    set_render_error,
    get_render_status,
)
from app.services.render_status import (
    reset_render_status, render_status)


app = FastAPI(
    title="Whisk Render Service",
    version="1.0"
)

cleanup_old_files()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "https://whiskeditor.vercel.app"
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/render-status")
async def get_render_status_route():

    return get_render_status()

@app.get("/")
def root():
    return {
        "status": "running",
        "service": "Whisk Render Service"
    }

@app.get("/health")
def health_check():
    return {
        "healthy": True
    }


def process_render(
    clip1,
    clip2,
    clip1_url,
    clip2_url,
    auto_sync,
    output_name,
):

    try:
        reset_render_status()
        start_render()

        clip1_path = resolve_media_input(
            clip1,
            clip1_url,
        )

        clip2_path = resolve_media_input(
            clip2,
            clip2_url,
        )

        if auto_sync:
            set_sync_stage()

        set_render_stage()

        output_path = render_side_by_side(
            clip1_path,
            clip2_path,
            output_name=output_name,
            enable_auto_sync=auto_sync,
        )

        set_finalize_stage()

        render_status["download_url"] = (
            f"/download/{output_path.name}"
        )

        render_status["output_filename"] = (
            output_path.name
        )

        finish_render()

    except Exception as e:

        set_render_error(str(e))

@app.post("/render")
async def render(

    background_tasks: BackgroundTasks,

    clip1: UploadFile | None = File(None),
    clip2: UploadFile | None = File(None),

    clip1_url: str | None = Form(None),
    clip2_url: str | None = Form(None),

    auto_sync: bool = Form(True),

    output_name: str = Form(...),
):
    if render_status["is_rendering"]:

        raise HTTPException(
            status_code=409,
            detail="Render already in progress"
        )
    
    background_tasks.add_task(

        process_render,

        clip1,
        clip2,
        clip1_url,
        clip2_url,
        auto_sync,
        output_name,
    )

    return {
        "success": True
    }


@app.get("/download/{filename}")
async def download_video(filename: str):

    file_path = OUTPUT_DIR / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=filename
    )

@app.post("/upload-youtube")
async def upload_to_youtube(

    filename: str = Form(...),

    title: str = Form(...),
):

    file_path = OUTPUT_DIR / filename

    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Rendered file not found"
        )

    try:

        youtube_url = upload_video(
            file_path,
            title,
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return {
        "youtube_url": youtube_url
    }