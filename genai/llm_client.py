
from genai.gemini_client import generate_response


SYSTEM_CONTEXT = """
You are GROHM AI, an assistant for GROHM Crypto Trading Bot S2.

The project includes:
1. Market Data Agent
2. Data Validation Agent
3. Indicator Agent
4. Candlestick Agent
5. Flexi Matrix Analyzer
6. Risk Management Agent
7. Paper Trading Agent
8. Trade Monitoring Agent
9. Performance Analysis Agent
10. Machine Learning Models
11. AI Modules

Explain technical concepts in simple language.
Do not invent project results.
Do not guarantee profits.
Never execute trades.
"""


def ask_grohm_ai(question: str) -> str:

    if not question or not question.strip():
        raise ValueError("Please enter a question.")

    prompt = f"""
    {SYSTEM_CONTEXT}

    User Question:
    {question}
    """

    return generate_response(prompt)


