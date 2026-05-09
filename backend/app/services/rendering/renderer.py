from pathlib import Path

import subprocess
import uuid

from app.services.media_analysis.trim_calculator import (
    calculate_trim_start
)


OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def render_side_by_side(
    clip1_path: Path,
    clip2_path: Path,
    enable_auto_sync: bool = True,
    preroll_seconds: float = 5.0
):

    #
    # Synchronization analysis
    #

    if enable_auto_sync:

        clip1_sync = calculate_trim_start(
            clip1_path,
            preroll_seconds
        )

        clip2_sync = calculate_trim_start(
            clip2_path,
            preroll_seconds
        )

        clip1_trim = clip1_sync[
            "trim_start"
        ]

        clip2_trim = clip2_sync[
            "trim_start"
        ]

        print("\n=== AUTO SYNC ===")

        print(
            f"Clip 1 Trim: "
            f"{clip1_trim:.2f}s"
        )

        print(
            f"Clip 2 Trim: "
            f"{clip2_trim:.2f}s"
        )

        print(
            f"Clip 1 Event: "
            f"{clip1_sync['reset_event']}"
        )

        print(
            f"Clip 2 Event: "
            f"{clip2_sync['reset_event']}"
        )

    else:

        clip1_trim = 0
        clip2_trim = 0

    #
    # Output file
    #

    output_filename = (
        f"{uuid.uuid4()}.mp4"
    )

    output_path = (
        OUTPUT_DIR / output_filename
    )

    #
    # FFmpeg command
    #

    ffmpeg_command = [

        "ffmpeg",

        "-y",

        #
        # Clip 1
        #

        "-ss",
        str(clip1_trim),

        "-i",
        str(clip1_path),

        #
        # Clip 2
        #

        "-ss",
        str(clip2_trim),

        "-i",
        str(clip2_path),

        #
        # Video stacking
        #

        "-filter_complex",

        (
            "[0:v]scale=960:540[left];"

            "[1:v]scale=960:540[right];"

            "[left][right]"
            "hstack=inputs=2[v]"
        ),

        #
        # Output mapping
        #

        "-map",
        "[v]",

        #
        # Audio from clip1
        #

        "-map",
        "0:a?",

        #
        # Encoding
        #

        "-c:v",
        "libx264",

        "-c:a",
        "aac",

        "-preset",
        "fast",

        "-crf",
        "23",

        "-shortest",

        #
        # Better browser playback
        #

        "-movflags",
        "+faststart",

        #
        # Output
        #

        str(output_path)
    ]

    #
    # Debug logging
    #

    print("\n=== FFMPEG COMMAND ===")

    print(
        " ".join(ffmpeg_command)
    )

    #
    # Execute FFmpeg
    #

    try:

        subprocess.run(
            ffmpeg_command,
            check=True,
            capture_output=True,
            text=True
        )

    except subprocess.CalledProcessError as e:

        print("\n=== FFMPEG ERROR ===")

        print(e.stderr)

        raise RuntimeError(
            f"FFmpeg render failed:\n"
            f"{e.stderr}"
        )

    #
    # Success
    #

    print("\n=== RENDER COMPLETE ===")

    print(
        f"Output: {output_path}"
    )

    return output_path