from pathlib import Path

import cv2
import numpy as np
from app.services.media_analysis.metadata import (
    get_video_metadata
)

def detect_white_flashes(
    video_path: Path,
    brightness_threshold: float = 240,
    white_ratio_threshold: float = 0.75,
    sample_rate: int = 5
):

    flashes = []

    cap = cv2.VideoCapture(
        str(video_path)
    )

    metadata = get_video_metadata(
        video_path
    )

    fps = metadata["fps"]

    frame_interval = max(
        int(fps / sample_rate),
        1
    )

    frame_index = 0

    while True:

        success, frame = cap.read()

        if not success:
            break

        #
        # Only sample every Nth frame
        #

        if frame_index % frame_interval != 0:
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
        # Calculate bright pixels
        #

        white_pixels = np.sum(
            gray >= brightness_threshold
        )

        total_pixels = gray.size

        white_ratio = (
            white_pixels / total_pixels
        )

        #
        # Flash detected
        #

        if white_ratio >= white_ratio_threshold:

            timestamp = (
                frame_index / fps
            )

            flashes.append({
                "frame_index": frame_index,
                "timestamp": timestamp,
                "white_ratio": white_ratio
            })

        frame_index += 1

    cap.release()

    return flashes  