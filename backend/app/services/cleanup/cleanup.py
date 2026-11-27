import json
import shutil
import time

from ..storage.paths import ACTIVE_JOB_IDS, JOBS_DIR, JOB_RETENTION_HOURS


def cleanup_old_files(max_age_hours: int = JOB_RETENTION_HOURS) -> None:
    """Remove expired per-job folders, preserving renders currently in flight."""
    cutoff = time.time() - max_age_hours * 60 * 60
    JOBS_DIR.mkdir(parents=True, exist_ok=True)

    for job_dir in JOBS_DIR.iterdir():
        if not job_dir.is_dir() or job_dir.name in ACTIVE_JOB_IDS:
            continue

        try:
            manifest_path = job_dir / "manifest.json"
            last_updated = manifest_path.stat().st_mtime if manifest_path.is_file() else job_dir.stat().st_mtime
            if last_updated < cutoff:
                shutil.rmtree(job_dir)
        except FileNotFoundError:
            continue


def write_job_manifest(job_dir, **updates) -> dict:
    manifest_path = job_dir / "manifest.json"
    manifest = {}
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            manifest = {}

    manifest.update(updates)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = manifest_path.with_suffix(".json.tmp")
    temporary_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    temporary_path.replace(manifest_path)
    return manifest
