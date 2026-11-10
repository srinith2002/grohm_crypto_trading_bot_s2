
import pandas as pd
from pathlib import Path
from transformers import pipeline

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = BASE_DIR / "data/crypto_news.csv"
OUTPUT_FILE = BASE_DIR / "data/candles/BTCUSD_30m_sentiment.csv"


def run_sentiment_agent():

    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"News file not found: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE)

    if df.empty or "Headline" not in df.columns:
        raise ValueError("News file is empty or Headline column is missing.")

    df = df.dropna(subset=["Headline"]).copy()

    if df.empty:
        raise ValueError("No valid headlines available.")

    print("Loading FinBERT model...")

    sentiment_model = pipeline(
        "text-classification",
        model="ProsusAI/finbert"
    )

    results = sentiment_model(
        df["Headline"].astype(str).tolist(),
        truncation=True
    )

    df["Sentiment"] = [item["label"].upper() for item in results]
    df["Confidence"] = [item["score"] for item in results]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print("\nGROHM NLP SENTIMENT RESULTS")
    print(df.to_string(index=False))

    print("\nSaved:", OUTPUT_FILE)


if __name__ == "__main__":
    run_sentiment_agent()
