from pathlib import Path
import subprocess
from urllib.parse import urlparse

from ..storage.paths import MAX_UPLOAD_BYTES

ALLOWED_HOSTS = {"medal.tv", "www.medal.tv"}


def download_medal_clip(url: str, output_path: Path) -> Path:
    parsed = urlparse(url.strip())
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError("Use a Medal.tv clip URL")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    command = [
        "yt-dlp",
        "--no-playlist",
        "--no-part",
        "--max-filesize",
        str(MAX_UPLOAD_BYTES),
        "--merge-output-format",
        "mp4",
        "-o",
        str(output_path),
        url.strip(),
    ]

    try:
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=900,
        )

    except subprocess.TimeoutExpired as error:
        output_path.unlink(missing_ok=True)
        raise RuntimeError("Medal.tv clip download timed out") from error

    except subprocess.CalledProcessError as e:
        output_path.unlink(missing_ok=True)
        raise RuntimeError(
            "Medal.tv clip download failed. Check that the clip is public and the URL is valid."
        ) from e

    if not output_path.is_file():
        raise RuntimeError("Medal.tv did not provide a downloadable MP4 clip")

    if output_path.stat().st_size > MAX_UPLOAD_BYTES:
        output_path.unlink(missing_ok=True)
        raise ValueError("Each clip must be 200 MB or smaller")

    return output_path
