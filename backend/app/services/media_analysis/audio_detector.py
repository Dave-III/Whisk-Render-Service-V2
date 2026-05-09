from pathlib import Path

import librosa
import numpy as np
from app.services.media_analysis.metadata import (
    get_video_metadata
)

def detect_audio_spikes(
    video_path: Path,
    spike_threshold: float = 0.2
):
    metadata = get_video_metadata(
        video_path
    )

    fps = metadata["fps"]


    audio, sr = librosa.load(
        str(video_path),
        sr=None
    )

    #
    # RMS volume
    #

    rms = librosa.feature.rms(
        y=audio
    )[0]

    #
    # Convert frames to timestamps
    #

    times = librosa.times_like(
        rms,
        sr=sr
    )

    spikes = []

    for i in range(len(rms)):

        if rms[i] >= spike_threshold:

            timestamp = float(times[i])

            frame_index = int(
                timestamp * fps
            )

            spikes.append({
                "frame_index": frame_index,
                "timestamp": timestamp,
                "strength": float(rms[i])
            })

    return spikes