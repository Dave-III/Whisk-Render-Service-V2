from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from pathlib import Path
import os
import pickle


SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def get_youtube_service():

    credentials = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    if not credentials:

        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json",
            SCOPES
        )

        credentials = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    return build(
        "youtube",
        "v3",
        credentials=credentials
    )

def upload_video(video_path: Path,title: str) -> str:

    youtube = get_youtube_service()

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": "Automatically rendered by Whisk Render Service"
            },
            "status": {
                "privacyStatus": "unlisted"
            }
        },
        media_body=MediaFileUpload(
            str(video_path),
            resumable=True
        )
    )

    response = request.execute()

    video_id = response["id"]

    return f"https://youtu.be/{video_id}"