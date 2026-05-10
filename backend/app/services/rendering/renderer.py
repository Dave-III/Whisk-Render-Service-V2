import re
import subprocess
from pathlib import Path

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

        clip1_sync = calculate_trim_start(clip1_path, preroll_seconds)
        clip2_sync = calculate_trim_start(clip2_path, preroll_seconds)

        clip1_trim = clip1_sync["trim_start"]
        clip2_trim = clip2_sync["trim_start"]

        print("\n=== AUTO SYNC ===")
        print(f"Clip 1 Trim: {clip1_trim:.2f}s")
        print(f"Clip 2 Trim: {clip2_trim:.2f}s")
        print(f"Clip 1 Event: {clip1_sync['reset_event']}")
        print(f"Clip 2 Event: {clip2_sync['reset_event']}")

    else:
        clip1_trim = 0
        clip2_trim = 0

    clip1_metadata = get_video_metadata(clip1_path)
    clip2_metadata = get_video_metadata(clip2_path)

    print("\n--- CLIP 1 METADATA ---")
    print(clip1_metadata)

    print("\n--- CLIP 2 METADATA ---")
    print(clip2_metadata)

    #
    # Target FPS — use the lower of the two clips
    #

    target_fps = min(
        round(clip1_metadata["fps"]),
        round(clip2_metadata["fps"])
    )

    if target_fps <= 0:
        target_fps = 30

    print(f"\n=== TARGET FPS ===\n{target_fps}")

    #
    # Output duration — trim both clips to the same length
    #

    clip1_remaining = clip1_metadata["duration"] - clip1_trim
    clip2_remaining = clip2_metadata["duration"] - clip2_trim
    output_duration = min(clip1_remaining, clip2_remaining)

    print(f"\n=== OUTPUT DURATION ===\n{output_duration:.2f}s")

    #
    # Pre-seek to 5s before trim point (lands on a keyframe),
    # then fine-trim the remaining gap inside the filter graph.
    # This avoids the massive frame-drop caused by seeking to
    # a non-keyframe boundary.
    #

    pre_seek1 = max(0, clip1_trim - 5)
    pre_seek2 = max(0, clip2_trim - 5)

    filter_trim1 = clip1_trim - pre_seek1
    filter_trim2 = clip2_trim - pre_seek2

    #
    # Safe output filename — strip special chars including spaces
    #

    safe_name = re.sub(r'[<> :"/\\|?*]', "_", output_name)
    output_filename = f"{safe_name}.mp4"
    output_path = OUTPUT_DIR / output_filename

    #
    # FFmpeg command
    #

    ffmpeg_command = [
        "ffmpeg",
        "-y",

        # Fast pre-seek before input (lands on keyframe)
        "-ss", str(pre_seek1),
        "-i", str(clip1_path),

        "-ss", str(pre_seek2),
        "-i", str(clip2_path),

        "-filter_complex",
        (
            # Fine-trim + duration cap + scale for clip 1
            f"[0:v]trim=start={filter_trim1}:duration={output_duration},"
            f"setpts=PTS-STARTPTS,scale=960:540[left];"

            # Fine-trim + duration cap + scale for clip 2
            f"[1:v]trim=start={filter_trim2}:duration={output_duration},"
            f"setpts=PTS-STARTPTS,scale=960:540[right];"

            # Audio trim from clip 1 only
            f"[0:a]atrim=start={filter_trim1}:duration={output_duration},"
            f"asetpts=PTS-STARTPTS[a];"

            # Stack clips side by side
            "[left][right]hstack=inputs=2[stacked];"

            # Pad to 1920x1080 with dark background
            "[stacked]pad=1920:1080:60:287:0x1a1a2e[v]"
        ),

        # Map filtered video and audio only (no duplicate raw audio map)
        "-map", "[v]",
        "-map", "[a]",

        # Video codec
        "-c:v", "libx264",
        "-r", str(target_fps),
        "-fps_mode", "cfr",

        # Audio codec
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-ac", "2",

        # Performance / quality
        "-preset", "veryfast",
        "-crf", "23",

        # Better browser playback
        "-movflags", "+faststart",

        str(output_path)
    ]

    #
    # Debug logging
    #

    print("\n=== FFMPEG COMMAND ===")
    print(" ".join(ffmpeg_command))

    #
    # Execute FFmpeg
    #

    try:
        audio_test = subprocess.run(
            [
                "ffprobe", "-i", str(clip1_path),
                "-show_streams", "-select_streams", "a",
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
                "ffprobe", "-i", str(output_path),
                "-show_streams", "-select_streams", "a",
            ]
        )

    except subprocess.CalledProcessError as e:
        print("\n=== FFMPEG ERROR ===")
        print(e.stderr)
        raise RuntimeError(f"FFmpeg render failed:\n{e.stderr}")

    #
    # Success
    #

    print(f"\n=== RENDER COMPLETE ===\nOutput: {output_path}")

    return output_path