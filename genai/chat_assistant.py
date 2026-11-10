from genai.gemini_client import generate_response


def ask_grohm_ai(question: str) -> str:

    if not question or not question.strip():
        raise ValueError("Please enter a question.")

    return generate_response(question)
