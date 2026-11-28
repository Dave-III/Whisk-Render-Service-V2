import threading


_lock = threading.Lock()
_statuses: dict[str, dict] = {}
_latest_job_id = ""


def reset_render_status(job_id: str) -> None:
    global _latest_job_id
    with _lock:
        _latest_job_id = job_id
        _statuses[job_id] = {
            "stage": "Queued...",
            "progress": 0,
            "is_rendering": True,
            "state": "queued",
            "error": None,
            "download_url": "",
            "output_filename": "",
            "job_id": job_id,
        }


def _update(job_id: str, values: dict) -> None:
    with _lock:
        if job_id in _statuses:
            _statuses[job_id].update(values)


def start_render(job_id: str) -> None:
    _update(job_id, {"stage": "Preparing clips...", "progress": 5, "is_rendering": True, "state": "rendering", "error": None})


def set_sync_stage(job_id: str) -> None:
    _update(job_id, {"stage": "Syncing runs...", "progress": 25})


def set_render_stage(job_id: str) -> None:
    _update(job_id, {"stage": "Rendering final video...", "progress": 70})


def set_finalize_stage(job_id: str) -> None:
    _update(job_id, {"stage": "Finalizing output...", "progress": 90})


def finish_render(job_id: str, download_url: str, output_filename: str) -> None:
    _update(job_id, {
        "stage": "Render complete!",
        "progress": 100,
        "is_rendering": False,
        "state": "complete",
        "download_url": download_url,
        "output_filename": output_filename,
    })


def set_render_error(job_id: str, message: str) -> None:
    _update(job_id, {"stage": "Error", "progress": 0, "is_rendering": False, "state": "failed", "error": message})


def get_render_status(job_id: str | None = None) -> dict:
    with _lock:
        selected_job_id = job_id or _latest_job_id
        status = _statuses.get(selected_job_id)
        if status is None:
            return {
                "stage": "Idle",
                "progress": 0,
                "is_rendering": False,
                "state": "idle",
                "error": None,
                "download_url": "",
                "output_filename": "",
                "job_id": selected_job_id,
            }
        return status.copy()
