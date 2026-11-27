from pathlib import Path

from fastapi import UploadFile

from ..medal.downloader import download_medal_clip
from ..storage.paths import MAX_UPLOAD_BYTES
from ..storage.saver import save_upload_file, upload_destination

def validate_upload_file(upload_file: UploadFile) -> None:
    if upload_file.content_type not in {"video/mp4", "application/octet-stream"}:
        raise ValueError("Only MP4 clips are supported")

    upload_file.file.seek(0, 2)
    file_size = upload_file.file.tell()
    upload_file.file.seek(0)
    if file_size > MAX_UPLOAD_BYTES:
        raise ValueError("Each clip must be 200 MB or smaller")

def resolve_media_input(
    upload_file: UploadFile | None,
    medal_url: str | None,
    destination: Path,
) -> Path:

    if upload_file:

        validate_upload_file(
            upload_file
        )

        return save_upload_file(upload_file, upload_destination(destination))

    if medal_url:
        return download_medal_clip(medal_url, upload_destination(destination))

    raise ValueError(
        "Either an MP4 upload or a Medal.tv URL is required"
    )
