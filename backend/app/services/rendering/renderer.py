from pathlib import Path

import subprocess
import uuid

from app.services.media_analysis.trim_calculator import (
    calculate_trim_start
)
from app.services.media_analysis.metadata import (
    get_video_metadata
)


OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def render_side_by_side(
    clip1_path: Path,
    clip2_path: Path,
    output_name: str,
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

    clip1_metadata = get_video_metadata(
        clip1_path
    )

    clip2_metadata = get_video_metadata(
        clip2_path
    )

    print("\n--- CLIP 1 METADATA ---")
    print(clip1_metadata)

    print("\n--- CLIP 2 METADATA ---")
    print(clip2_metadata)



    target_fps = min(
        round(clip1_metadata["fps"]),
        round(clip2_metadata["fps"])
    )

    #
    # Safety fallback
    #

    if target_fps <= 0:
        target_fps = 30

    print(
        f"\n=== TARGET FPS ===\n"
        f"{target_fps}"
    )

    #
    # Output file
    #

    #
    # Safe output filename
    #
    import re
    safe_name = re.sub(
        r'[<>:"/\\\\|?*]',
        "_",
        output_name
    )

    output_filename = (
        f"{safe_name}.mp4"
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

        "-ss",
        str(clip1_trim),

        "-i",
        str(clip1_path),

        "-ss",
        str(clip2_trim),

        "-i",
        str(clip2_path),

        "-loop",
        "1",

        "-i",
        "assets/background.png",
        #
        # Video stacking
        #

        "-filter_complex",

        (
            #
            # Background canvas
            #

            "[2:v]scale=1920:1080,format=yuv420p[bg];"

            #
            # Left clip
            #

            "[0:v]"
            "scale=900:506"
            "[left];"

            #
            # Right clip
            #

            "[1:v]"
            "scale=900:506"
            "[right];"

            #
            # Overlay left clip
            #

            "[bg][left]"
            "overlay=x=40:y=287"
            "[temp];"

            #
            # Overlay right clip
            #

            "[temp][right]"
            "overlay=x=980:y=287"
            "[v]"
        ),

        #
        # Output mapping
        #

        "-map",
        "[v]",

        #
        # Explicit audio track from clip1
        #

        "-map",
        "0:a:0?",

        #
        # Video codec
        #

        "-c:v",
        "libx264",

        "-r",
        str(target_fps),

        "-fps_mode",
        "cfr",

        #
        # Audio codec
        #

        "-c:a",
        "aac",

        #
        # Audio bitrate
        #

        "-b:a",
        "192k",

        #
        # Audio compatibility
        #

        "-ar",
        "48000",

        "-ac",
        "2",

        #
        # Performance
        #

        "-preset",
        "veryfast",

        #
        # Quality
        #

        "-crf",
        "23",

        #
        # Sync handling
        #

        "-shortest",

        #
        # Better browser playback
        #

        "-movflags",
        "+faststart",

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
        audio_test = subprocess.run(

            [
                "ffprobe",
                "-i",
                str(clip1_path),
                "-show_streams",
                "-select_streams",
                "a",
            ],

            capture_output=True,
            text=True,
        )

        print("\n=== AUDIO STREAMS ===")
        print(audio_test.stdout)

        subprocess.run(
            ffmpeg_command,
            check=True,
            capture_output=True,
            text=True
        )
        print("\n=== OUTPUT AUDIO TEST ===")

        subprocess.run(
            [
                "ffprobe",
                "-i",
                str(output_path),
                "-show_streams",
                "-select_streams",
                "a",
            ]
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