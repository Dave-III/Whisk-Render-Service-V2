from fastapi import UploadFile
from pathlib import Path
import shutil
import uuid

MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def save_upload_file(upload_file: UploadFile) -> Path:

    contents = upload_file.file.read()

    if len(contents) > MAX_FILE_SIZE:

        raise ValueError(
            "File exceeds 500MB limit"
        )

    upload_file.file.seek(0)

    filename = f"{uuid.uuid4()}_{upload_file.filename}"

    file_path = UPLOAD_DIR / filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return file_path