
import os
import time

from google import genai
from google.genai import types
from genai.config import GEMINI_MODEL


def generate_response(prompt: str) -> str:

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=30000
        )
    )

    max_attempts = 3

    try:
        for attempt in range(max_attempts):

            try:
                response = client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt
                )

                if not response.text:
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                return response.text

            except Exception as error:

                error_message = str(error)

                temporary_error = (
                    "503" in error_message
                    or "UNAVAILABLE" in error_message
                    or "429" in error_message
                    or "RESOURCE_EXHAUSTED" in error_message
                )

                if temporary_error and attempt < max_attempts - 1:
                    time.sleep(2 ** (attempt + 1))
                    continue

                if temporary_error:
                    return (
                        "Gemini is temporarily busy. "
                        "Please try again later."
                    )

                return f"Gemini connection error: {error_message}"

    finally:
        client.close()



