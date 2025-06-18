
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
        },
        "status": {"privacyStatus": "public"},
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)