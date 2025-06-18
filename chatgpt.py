import os
from typing import List, Tuple
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT_TEMPLATE = (
    "You are a creative social media assistant. "
    "Given the following challenge description, generate a short caption "
    "for a video and provide 5 relevant hashtags. "
    "Respond in the format:\n"
    "Caption: <caption>\n"
    "Hashtags: #tag1 #tag2 #tag3 #tag4 #tag5"
)


def generate_caption_and_hashtags(challenge: str) -> Tuple[str, List[str]]:
    """Use ChatGPT to create a caption and hashtags for the challenge."""
    if not openai.api_key:
        raise RuntimeError("OPENAI_API_KEY not configured")

    prompt = f"{PROMPT_TEMPLATE}\n\nChallenge: {challenge}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    text = response.choices[0].message["content"].strip()
    caption = ""
    hashtags: List[str] = []
    for line in text.splitlines():
        if line.lower().startswith("caption:"):
            caption = line.split(":", 1)[1].strip()
        if line.lower().startswith("hashtags:"):
            tags = line.split(":", 1)[1].strip()
            hashtags = [tag.strip() for tag in tags.split() if tag.startswith("#")]
    return caption, hashtags
