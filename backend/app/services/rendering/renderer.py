import subprocess
from pathlib import Path

from app.services.media_analysis.trim_calculator import (
    calculate_trim_start
)
from app.services.media_analysis.metadata import (
    get_video_metadata
)


BACKGROUND_IMAGE = (
    Path(__file__).resolve().parents[3]
    / "assets"
    / "watercolor-video-background.jfif"
)


def render_side_by_side(
    clip1_path: Path,
    clip2_path: Path,
    output_name: str,
    output_dir: Path,
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

    if not BACKGROUND_IMAGE.is_file():
        raise RuntimeError(f"Render background image not found: {BACKGROUND_IMAGE}")

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

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / output_name

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

        # Loop the watercolor artwork as the video canvas background.
        "-loop", "1",
        "-framerate", str(target_fps),
        "-i", str(BACKGROUND_IMAGE),

        "-filter_complex",
        (
            # Fine-trim + duration cap + scale for clip 1
            f"[0:v]trim=start={filter_trim1}:duration={output_duration},"
            f"setpts=PTS-STARTPTS,scale=900:506[left];"

            # Fine-trim + duration cap + scale for clip 2
            f"[1:v]trim=start={filter_trim2}:duration={output_duration},"
            f"setpts=PTS-STARTPTS,scale=900:506[right];"

            # Audio trim from clip 1 only
            f"[0:a]atrim=start={filter_trim1}:duration={output_duration},"
            f"asetpts=PTS-STARTPTS[a];"

            # Stack clips side by side
            "[left][right]hstack=inputs=2[clips];"

            # Use the artwork as a full-frame background and center the clips over it.
            f"[2:v]scale=1920:1080:flags=lanczos,setsar=1,"
            f"trim=duration={output_duration},setpts=PTS-STARTPTS[background];"
            "[background][clips]overlay=60:287:shortest=1,format=yuv420p[v]"
        ),

        # Map filtered video and audio only (no duplicate raw audio map)
        "-map", "[v]",
        "-map", "0:a:0?",

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

        result = subprocess.run(
            ffmpeg_command,
            capture_output=True,
            text=True,
            timeout=3600,
        )

        if result.returncode != 0:

            print("\n=== FFMPEG COMMAND ===")
            print(" ".join(ffmpeg_command))

            print("\n=== FFMPEG STDOUT ===")
            print(result.stdout)

            print("\n=== FFMPEG STDERR ===")
            print(result.stderr)

            raise RuntimeError(
                f"FFmpeg render failed:\n{result.stderr}"
            )

        print("\n=== OUTPUT AUDIO TEST ===")
        subprocess.run(
            [
                "ffprobe", "-i", str(output_path),
                "-show_streams", "-select_streams", "a",
            ]
        )

    except subprocess.TimeoutExpired as error:
        output_path.unlink(missing_ok=True)
        raise RuntimeError("FFmpeg render exceeded the one-hour limit") from error


    print(f"\n=== RENDER COMPLETE ===\nOutput: {output_path}")

    return output_path
