import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def check_configuration():
    return {
        "provider": "Google Gemini",
        "model": GEMINI_MODEL,
        "api_key_configured": bool(GEMINI_API_KEY)
    }
