render_status = {
    "stage": "Idle",
    "progress": 0,
    "is_rendering": False,
    "error": None,
    "download_url": "",
    "output_filename": "",
}


def reset_render_status():

    render_status["stage"] = "Idle"
    render_status["progress"] = 0
    render_status["is_rendering"] = False
    render_status["error"] = None
    render_status["download_url"] = ""
    render_status["output_filename"] = ""


def start_render():

    render_status["stage"] = (
        "Preparing clips..."
    )

    render_status["progress"] = 5

    render_status["is_rendering"] = True

    render_status["error"] = None


def set_sync_stage():

    render_status["stage"] = (
        "Syncing runs..."
    )

    render_status["progress"] = 25


def set_render_stage():

    render_status["stage"] = (
        "Rendering final video..."
    )

    render_status["progress"] = 70


def set_finalize_stage():

    render_status["stage"] = (
        "Finalizing output..."
    )

    render_status["progress"] = 90


def finish_render():

    render_status["stage"] = (
        "Render complete!"
    )

    render_status["progress"] = 100

    render_status["is_rendering"] = False


def set_render_error(
    message: str
):

    render_status["stage"] = "Error"

    render_status["progress"] = 0

    render_status["is_rendering"] = False

    render_status["error"] = message


def get_render_status():

    return render_status