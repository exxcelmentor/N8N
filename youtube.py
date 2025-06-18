"""YouTube upload helper.

This script authenticates with the Google API and uploads a video. It expects
OAuth credentials generated from Google's developer console. The first time you
run the script it will create a token file for subsequent use.

"""
import os
from pathlib import Path
from typing import List

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import config

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def get_youtube_service():
    """Return authenticated YouTube service using OAuth credentials."""
    token_path = Path(config.YOUTUBE_TOKEN_FILE)
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            config.YOUTUBE_CLIENT_SECRETS, SCOPES
        )
        creds = flow.run_console()
        token_path.write_text(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def upload_video(video_path: str, title: str, description: str, tags: List[str]) -> str:
    """Upload a video to YouTube and return the video URL."""
    if not Path(video_path).exists():
        raise FileNotFoundError(video_path)

    youtube = get_youtube_service()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
        },
        "status": {"privacyStatus": "public"},
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status", body=body, media_body=media
    )
    response = request.execute()
    return f"https://youtu.be/{response['id']}"


def main():
    """CLI entry point for uploading a video."""
    import argparse

    parser = argparse.ArgumentParser(description="Upload a video to YouTube")
    parser.add_argument("video", help="Path to the video file")
    parser.add_argument("title", help="Video title")
    parser.add_argument("--description", default="", help="Video description")
    parser.add_argument("--tags", nargs="*", default=[], help="Video tags")
    args = parser.parse_args()

    url = upload_video(args.video, args.title, args.description, args.tags)
    print(f"Uploaded video: {url}")


if __name__ == "__main__":
    main()
