from pathlib import Path
from fastapi import UploadFile
from ..storage.saver import (
    save_upload_file
)
from ..medal.downloader import (
    download_medal_clip
)
MAX_FILE_SIZE = 200 * 1024 * 1024 # 200MB

def validate_upload_file(
    upload_file: UploadFile
):

    upload_file.file.seek(0, 2)

    file_size = upload_file.file.tell()

    upload_file.file.seek(0)

    if file_size > MAX_FILE_SIZE:

        raise ValueError(
            f"File exceeds maximum size of 200MB"
        )

    allowed_types = [
        "video/mp4"
    ]

    if upload_file.content_type not in allowed_types:

        raise ValueError(
            "Only MP4 files are supported"
        )

def resolve_media_input(
    upload_file: UploadFile | None,
    medal_url: str | None
) -> Path:

    if upload_file:

        validate_upload_file(
            upload_file
        )

        return save_upload_file(
            upload_file
        )

    if medal_url:
        return download_medal_clip(medal_url)

    raise ValueError(
        "Either upload_file or medal_url must be provided"
    )