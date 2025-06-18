"""Configuration for API clients."""

from dotenv import load_dotenv
import os

load_dotenv()

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Google API settings
# Path to OAuth client secrets file downloaded from the Google Cloud console
YOUTUBE_CLIENT_SECRETS = os.getenv("YOUTUBE_CLIENT_SECRETS", "client_secrets.json")
# File where OAuth tokens will be stored
YOUTUBE_TOKEN_FILE = os.getenv("YOUTUBE_TOKEN_FILE", "token.json")
