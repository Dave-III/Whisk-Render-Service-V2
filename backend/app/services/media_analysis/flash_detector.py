from pathlib import Path

import cv2
import numpy as np

from app.services.media_analysis.metadata import (
    get_video_metadata
)


def detect_white_flashes(
        
    video_path: Path,
    brightness_threshold: float = 240,
    white_ratio_threshold: float = 0.80,
    sample_rate: int = 5,
    analysis_seconds: int = 60,
    minimum_gap_seconds: float = 1.5
):

    flashes = []

    #
    # Open video
    #

    cap = cv2.VideoCapture(
        str(video_path)
    )

    if not cap.isOpened():

        raise RuntimeError(
            f"Failed to open video: "
            f"{video_path}"
        )

    #
    # Metadata
    #

    metadata = get_video_metadata(
        video_path
    )

    fps = metadata["fps"]

    frame_count = metadata[
        "frame_count"
    ]

    duration = metadata[
        "duration"
    ]

    #
    # Begin analysis near end
    #

    start_frame = max(

        int(
            frame_count -
            (fps * analysis_seconds)
        ),

        0
    )

    #
    # Seek to analysis position
    #

    cap.set(
        cv2.CAP_PROP_POS_FRAMES,
        start_frame
    )

    #
    # Sampling interval
    #

    frame_interval = max(

        int(fps / sample_rate),

        1
    )

    #
    # Flash grouping
    #

    minimum_gap_frames = int(
        fps * minimum_gap_seconds
    )

    last_flash_frame = -999999

    #
    # IMPORTANT:
    # Start from analysis frame
    #

    frame_index = start_frame

    #
    # Debug
    #

    print("\n=== FLASH ANALYSIS ===")

    print(
        f"Duration: "
        f"{duration:.2f}s"
    )

    print(
        f"FPS: {fps}"
    )

    print(
        f"Frame Count: "
        f"{frame_count}"
    )

    print(
        f"Analysis Start Frame: "
        f"{start_frame}"
    )

    print(
        f"Analysis Start Time: "
        f"{start_frame / fps:.2f}s"
    )

    #
    # Main loop
    #

    while True:

        success, frame = cap.read()

        if not success:
            break

        #
        # Only sample every Nth frame
        #

        if (
            frame_index %
            frame_interval
            != 0
        ):

            frame_index += 1
            continue

        #
        # Convert to grayscale
        #

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        #
        # Calculate white ratio
        #

        white_pixels = np.sum(
            gray >= brightness_threshold
        )

        total_pixels = gray.size

        white_ratio = (
            white_pixels /
            total_pixels
        )

        #
        # Detect grouped flashes
        #

        if (

            white_ratio >=
            white_ratio_threshold

            and

            (
                frame_index -
                last_flash_frame
            ) >
            minimum_gap_frames
        ):

            timestamp = (
                frame_index / fps
            )

            flash = {

                "frame_index":
                    frame_index,

                "timestamp":
                    timestamp,

                "white_ratio":
                    float(white_ratio)
            }

            flashes.append(
                flash
            )

            last_flash_frame = (
                frame_index
            )

            #
            # Debug
            #

            print(

                f"FLASH DETECTED | "

                f"Frame: {frame_index} | "

                f"Time: {timestamp:.2f}s | "

                f"White Ratio: "
                f"{white_ratio:.2f}"
            )

        #
        # Advance frame counter
        #

        frame_index += 1

    #
    # Cleanup
    #

    cap.release()

    #
    # Sort newest first
    #

    flashes.sort(

        key=lambda x:
        x["timestamp"],

        reverse=True
    )

    #
    # Debug summary
    #

    print("\n=== FLASH SUMMARY ===")

    print(
        f"Detected "
        f"{len(flashes)} flashes"
    )

    return flashes