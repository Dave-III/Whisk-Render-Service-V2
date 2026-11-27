from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from .paths import MAX_UPLOAD_BYTES


def upload_destination(directory: Path) -> Path:
    return directory / f"{uuid4().hex}.mp4"


def save_upload_file(upload_file: UploadFile, destination: Path) -> Path:
    """Stream an uploaded MP4 to disk without buffering it a second time."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    size = 0

    try:
        with destination.open("wb") as output:
            while chunk := upload_file.file.read(1024 * 1024):
                size += len(chunk)
                if size > MAX_UPLOAD_BYTES:
                    raise ValueError("Each clip must be 200 MB or smaller")
                output.write(chunk)
    except Exception:
        destination.unlink(missing_ok=True)
        raise

    if size == 0:
        destination.unlink(missing_ok=True)
        raise ValueError("The uploaded clip is empty")

    return destination
