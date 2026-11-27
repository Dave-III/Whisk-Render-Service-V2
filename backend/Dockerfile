FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    WHISK_DATA_DIR=/tmp/whisk

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY assets ./assets

EXPOSE 8080

CMD ["sh", "-c", "umask 077; mkdir -p \"$WHISK_DATA_DIR/jobs\" \"$WHISK_DATA_DIR/secrets\"; if [ -n \"${CLIENT_SECRET_B64:-}\" ]; then printf '%s' \"$CLIENT_SECRET_B64\" | base64 -d > \"$WHISK_DATA_DIR/secrets/client_secret.json\"; fi; if [ -n \"${TOKEN_PICKLE_B64:-}\" ]; then printf '%s' \"$TOKEN_PICKLE_B64\" | base64 -d > \"$WHISK_DATA_DIR/secrets/token.pickle\"; fi; exec uvicorn app.main:app --host 0.0.0.0 --port \"${PORT:-8080}\""]
