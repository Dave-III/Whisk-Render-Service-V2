from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
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
async def render_video(

    clip1: UploadFile | None = File(None),
    clip2: UploadFile | None = File(None),

    clip1_url: str | None = Form(None),
    clip2_url: str | None = Form(None),

    level_name: str | None = Form(None),
    run_time: str | None = Form(None),

    foam_player: str | None = Form(None),
    luna_player: str | None = Form(None),
):
    cleanup_old_files()

    video_title = (
        f"{level_name} — "
        f"{run_time} | "
        f"Foam: {foam_player} | "
        f"Luna: {luna_player}"
    )

    if clip1 and clip1_url:
        raise HTTPException(
            status_code=400,
            detail="Provide either clip1 upload OR clip1_url, not both"
        )

    if not clip1 and not clip1_url:
        raise HTTPException(
            status_code=400,
            detail="clip1 upload or clip1_url is required"
        )


    if clip2 and clip2_url:
        raise HTTPException(
            status_code=400,
            detail="Provide either clip2 upload OR clip2_url, not both"
        )

    if not clip2 and not clip2_url:
        raise HTTPException(
            status_code=400,
            detail="clip2 upload or clip2_url is required"
        )

    clip1_path = resolve_media_input(
        clip1,
        clip1_url
)

    clip2_path = resolve_media_input(
        clip2,
        clip2_url
    )
    try:

        output_path = render_side_by_side(
            clip1_path,
            clip2_path
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return {
        "message": "Render completed successfully",
        "output_video": str(output_path),
        "download_url": f"/download/{output_path.name}",
        "youtube_url": None
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