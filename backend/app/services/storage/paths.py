"""Filesystem layout for transient Whisk render jobs."""

import os
from pathlib import Path


DATA_DIR = Path(os.getenv("WHISK_DATA_DIR", "/tmp/whisk")).expanduser().resolve()
JOBS_DIR = DATA_DIR / "jobs"
SECRETS_DIR = DATA_DIR / "secrets"
MAX_UPLOAD_BYTES = 200 * 1024 * 1024
JOB_RETENTION_HOURS = int(os.getenv("WHISK_JOB_RETENTION_HOURS", "2"))

for directory in (JOBS_DIR, SECRETS_DIR):
    directory.mkdir(parents=True, exist_ok=True)

# In-memory guard so the janitor never removes a render that is still running.
ACTIVE_JOB_IDS: set[str] = set()
