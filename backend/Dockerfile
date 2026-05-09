FROM python:3.11

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y coreutils

CMD echo $CLIENT_SECRET_B64 | base64 -d > client_secret.json && \
    echo $TOKEN_PICKLE_B64 | base64 -d > token.pickle && \
    uvicorn app.main:app --host 0.0.0.0 --port $PORT