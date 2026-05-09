from fastapi import FastAPI, UploadFile, File, Form, HTTPException
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
from app.services.uploads.saver import save_upload_file


app = FastAPI(
    title="Whisk Render Service",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/render-status")
async def render_status():

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

@app.post("/render")
async def render(
    clip1: UploadFile | None = File(None),
    clip2: UploadFile | None = File(None),

    clip1_url: str | None = Form(None),
    clip2_url: str | None = Form(None),

    auto_sync: bool = Form(True),
):

    try:

        start_render()

        # -----------------------------------
        # PREPARE CLIPS
        # -----------------------------------

        # -----------------------------------
        # CLIP 1
        # -----------------------------------

        if clip1_url:

            clip1_path = download_video(
                clip1_url
            )

        else:

            if clip1 is None:
                raise HTTPException(
                    status_code=400,
                    detail="Clip 1 missing",
                )

            clip1_path = await save_upload_file(
                clip1
            )

        # -----------------------------------
        # CLIP 2
        # -----------------------------------

        if clip2_url:

            clip2_path = download_video(
                clip2_url
            )

        else:

            if clip2 is None:
                raise HTTPException(
                    status_code=400,
                    detail="Clip 2 missing",
                )

            clip2_path = await save_upload_file(
                clip2
            )

        # -----------------------------------
        # AUTO SYNC
        # -----------------------------------

        if auto_sync:

            set_sync_stage()

            # future sync orchestration here
            # offsets = detect_sync(...)
            # trim clips here

        # -----------------------------------
        # RENDER
        # -----------------------------------

        set_render_stage()

        output_path = (
            OUTPUT_DIR /
            f"{uuid4()}.mp4"
        )

        render_side_by_side(
            left_video=clip1_path,
            right_video=clip2_path,
            output_path=output_path,
        )

        # -----------------------------------
        # FINALIZE
        # -----------------------------------

        set_finalize_stage()

        download_url = (
            f"/download/{output_path.name}"
        )

        finish_render()

        return {
            "success": True,

            "output_video":
                str(output_path),

            "download_url":
                download_url,
        }

    except Exception as e:

        set_render_error(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )



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
    filename: str = Form(...)
):

    file_path = OUTPUT_DIR / filename

    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Rendered file not found"
        )

    try:

        youtube_url = upload_video(file_path)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return {
        "youtube_url": youtube_url
    }