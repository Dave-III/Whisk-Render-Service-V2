from pathlib import Path

from app.services.media_analysis.sync_detector import (
    detect_reset_events
)


def calculate_trim_start(
    video_path: Path,
    preroll_seconds: float = 5.0
):

    reset_events = detect_reset_events(
        video_path
    )

    #
    # No reset found
    #

    if not reset_events:

        return {
            "trim_start": 0,
            "reset_event": None
        }

    #
    # Most recent event
    #

    latest_reset = reset_events[0]

    trim_start = max(
        latest_reset["timestamp"] - preroll_seconds,
        0
    )

    return {
        "trim_start": trim_start,
        "reset_event": latest_reset
    }