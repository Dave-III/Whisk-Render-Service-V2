from pathlib import Path
from datetime import datetime, timedelta


DIRECTORIES = [
    Path("uploads"),
    Path("temp"),
    Path("outputs")
]


def cleanup_old_files(
    max_age_hours: int = 1
):

    cutoff_time = datetime.now() - timedelta(
        hours=max_age_hours
    )

    for directory in DIRECTORIES:

        if not directory.exists():
            continue

        for file_path in directory.iterdir():

            if not file_path.is_file():
                continue

            modified_time = datetime.fromtimestamp(
                file_path.stat().st_mtime
            )

            if modified_time < cutoff_time:

                try:
                    file_path.unlink()

                    print(
                        f"Deleted old file: {file_path}"
                    )

                except Exception as e:

                    print(
                        f"Failed to delete {file_path}: {e}"
                    )