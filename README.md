# N8N Helpers

This repository includes small utilities for working with the content pipeline.

## API Client Configuration

The helper modules read configuration values from environment variables via
`config.py`. Create a `.env` file or set these variables in your environment:

```
OPENAI_API_KEY=your-openai-key
YOUTUBE_CLIENT_SECRETS=client_secrets.json
YOUTUBE_TOKEN_FILE=token.json
```

To generate the `client_secrets.json` and `token.json` for YouTube, create an
OAuth 2.0 client in the Google Cloud console and download the secret file. The
first time you run `youtube.py` it will prompt you to authorize access and store
the credentials in `token.json`.
