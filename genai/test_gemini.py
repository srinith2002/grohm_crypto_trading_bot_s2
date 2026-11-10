
import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not configured!")

client = genai.Client(api_key=api_key)

print("Gemini authentication configured successfully!")

