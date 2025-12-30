import os
import time
import requests
from dotenv import load_dotenv
from typing import Dict

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found")

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)


def call_llm(system_prompt: str, user_prompt: str, retries: int = 3) -> Dict[str, str]:
    full_prompt = f"{system_prompt}\n\nUSER QUERY:\n{user_prompt}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": full_prompt}
                ]
            }
        ]
    }

    for attempt in range(retries):
        response = requests.post(
            f"{GEMINI_URL}?key={API_KEY}",
            json=payload,
            timeout=30
        )

        # ✅ Success
        if response.status_code == 200:
            data = response.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return {
                "model": "gemini-2.5-flash",
                "response": text
            }

        # ⚠️ Rate limit → wait and retry
        if response.status_code in (429, 503):
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            time.sleep(wait_time)
            continue

        # ❌ Other errors
        response.raise_for_status()

    # ❌ All retries exhausted
    raise RuntimeError(
        "Rate limit exceeded. Please wait a moment and try again."
    )
