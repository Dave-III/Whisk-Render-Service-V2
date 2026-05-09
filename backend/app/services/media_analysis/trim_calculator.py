from pathlib import Path

from app.services.media_analysis.flash_detector import (
    detect_white_flashes
)


def calculate_trim_start(
    video_path: Path,
    preroll_seconds: float = 5.0
):

    flashes = detect_white_flashes(
        video_path
    )

    #
    # No flashes found
    #

    if not flashes:

        print(
            "\nNo flashes detected"
        )

        return {

            "trim_start": 0,

            "reset_event": None
        }

    #
    # Most recent flash
    #

    latest_flash = flashes[0]

    trim_start = max(

        latest_flash[
            "timestamp"
        ] - preroll_seconds,

        0
    )

    #
    # Debug
    #

    print("\n=== TRIM CALCULATION ===")

    print(
        f"Latest Flash: "
        f"{latest_flash}"
    )

    print(
        f"Trim Start: "
        f"{trim_start:.2f}s"
    )

    return {

        "trim_start":
            trim_start,

        "reset_event":
            latest_flash
    }