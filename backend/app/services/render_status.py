render_status = {
    "stage": "Idle",
    "progress": 0,
    "is_rendering": False,
    "error": None,
    "download_url": "",
    "output_filename": "",
    "job_id": "",
}


def reset_render_status(job_id: str = "") -> None:
    render_status.update({
        "stage": "Idle",
        "progress": 0,
        "is_rendering": False,
        "error": None,
        "download_url": "",
        "output_filename": "",
        "job_id": job_id,
    })


def start_render() -> None:
    render_status.update({"stage": "Preparing clips...", "progress": 5, "is_rendering": True, "error": None})


def set_sync_stage() -> None:
    render_status.update({"stage": "Syncing runs...", "progress": 25})


def set_render_stage() -> None:
    render_status.update({"stage": "Rendering final video...", "progress": 70})


def set_finalize_stage() -> None:
    render_status.update({"stage": "Finalizing output...", "progress": 90})


def finish_render() -> None:
    render_status.update({"stage": "Render complete!", "progress": 100, "is_rendering": False})


def set_render_error(message: str) -> None:
    render_status.update({"stage": "Error", "progress": 0, "is_rendering": False, "error": message})


def get_render_status() -> dict:
    return render_status.copy()
