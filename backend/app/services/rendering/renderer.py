from pathlib import Path
import subprocess
import uuid


OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def render_side_by_side(
    clip1_path: Path,
    clip2_path: Path
) -> Path:

    output_filename = f"{uuid.uuid4()}.mp4"
    output_path = OUTPUT_DIR / output_filename

    ffmpeg_command = [
        "ffmpeg",
        "-y",

        "-i", str(clip1_path),
        "-i", str(clip2_path),

        "-loop", "1",
        "-i", "assets/background.png",

        "-filter_complex",
        (
            "[0:v]scale=960:-2[left];"

            "[1:v]scale=960:-2[right];"

            "[left][right]hstack=inputs=2[stacked];"

            "[2:v]scale=1920:1080[bg];"

            "[bg][stacked]overlay=(W-w)/2:(H-h)/2[v]"
        ),

        "-map", "[v]",
        "-map", "0:a?",

        "-c:v", "libx264",
        "-c:a", "aac",

        "-preset", "fast",
        "-crf", "23",

        "-shortest",

        "-movflags", "+faststart",

        str(output_path)
    ]

    try:
        subprocess.run(
            ffmpeg_command,
            check=True,
            capture_output=True,
            text=True
        )

    except subprocess.CalledProcessError as e:

        print(e.stderr)

        raise RuntimeError(
            f"FFmpeg render failed:\n{e.stderr}"
        )

    return output_path