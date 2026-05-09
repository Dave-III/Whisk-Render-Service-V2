from pathlib import Path

from app.services.media_analysis.flash_detector import (
    detect_white_flashes
)

from app.services.media_analysis.audio_detector import (
    detect_audio_spikes
)


def detect_reset_events(
    video_path: Path,
    max_delta: float = 0.5
):

    flashes = detect_white_flashes(
        video_path
    )

    spikes = detect_audio_spikes(
        video_path
    )

    reset_events = []

    for flash in flashes:

        flash_time = flash["timestamp"]

        for spike in spikes:

            spike_time = spike["timestamp"]

            delta = abs(
                flash_time - spike_time
            )

            #
            # Matched audiovisual event
            #

            if delta <= max_delta:

                confidence = (
                    flash["white_ratio"] *
                    spike["strength"]
                )

                reset_events.append({
                    "frame_index": flash["frame_index"],
                    "timestamp": flash_time,
                    "confidence": confidence,
                    "white_ratio": flash["white_ratio"],
                    "audio_strength": spike["strength"]
                })

                break

    #
    # Sort newest first
    #

    reset_events.sort(
        key=lambda x: x["timestamp"],
        reverse=True
    )

    return reset_events