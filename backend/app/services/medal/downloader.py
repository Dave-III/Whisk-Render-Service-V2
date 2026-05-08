from pathlib import Path
import subprocess
import uuid


DOWNLOAD_DIR = Path("temp")
DOWNLOAD_DIR.mkdir(exist_ok=True)


def download_medal_clip(url: str) -> Path:

    output_filename = f"{uuid.uuid4()}.mp4"
    output_path = DOWNLOAD_DIR / output_filename

    command = [
        "yt-dlp",
        "-o",
        str(output_path),
        url
    ]

    try:
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )

    except subprocess.CalledProcessError as e:

        print(e.stderr)

        raise RuntimeError(
            f"yt-dlp download failed:\n{e.stderr}"
        )

    return output_path