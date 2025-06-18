import os
from pathlib import Path
from typing import List
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def upload_video(video_path: str, title: str, description: str, tags: List[str]) -> str:
    """Upload a video to YouTube and return the video URL."""
    creds_path = os.environ.get("YOUTUBE_TOKEN_FILE", "token.json")
    if not Path(video_path).exists():
        raise FileNotFoundError(video_path)

    creds = Credentials.from_authorized_user_file(creds_path, SCOPES)
    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
        },
        "status": {"privacyStatus": "public"},
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    return f"https://youtu.be/{response['id']}"
