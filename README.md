# Whisk

Whisk is split into a Next.js editor and an isolated FastAPI/FFmpeg rendering API.

## Repository layout

- `frontend/` — Next.js editor UI.
- `backend/` — Railway rendering service, Dockerfile, runtime dependencies, and API code.
- `backend/app/services/` — input validation, Medal downloads, media analysis, rendering, cleanup, storage, and YouTube upload.

Use `backend/requirements.txt` as the single Python dependency manifest. Do not use a workstation-wide `pip freeze` in the repository root.

## Backend deployment

The existing Railway service is linked to `Dave-III/Whisk-Render-Service-V2` on `main`, with service root directory `backend`. The Dockerfile listens on Railway's assigned `PORT` (fallback 8080). Set the Railway health check to `/health`. Keep the existing YouTube credential variables in Railway Variables; do not commit or copy their values into this repository.

The API accepts MP4 clips or Medal.tv links and emits MP4 renders. Runtime files use the documented per-job JSON/MP4 layout in [`backend/README.md`](backend/README.md). Jobs expire after two hours by default. Railway's container filesystem is temporary, so a deployment or restart can remove files earlier; there is no persistent volume configured.

Optional backend settings are `WHISK_DATA_DIR`, `WHISK_JOB_RETENTION_HOURS`, and `WHISK_ALLOWED_ORIGINS`. CORS credentials are disabled. The default origin policy is `*` for the current credential-free browser API; set a comma-separated allowlist once the final frontend origin is known.

## Frontend

Set `NEXT_PUBLIC_API_URL` in the frontend hosting project to the Railway backend URL. The frontend is a separate deployment and is not changed by Railway backend releases.
