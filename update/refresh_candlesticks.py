import pandas as pd
from pathlib import Path

from agents.candlestick_agent import identify_candlestick_patterns

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = PROJECT_ROOT / "data" / "candles" / "BTCUSD_30m.csv"

OUTPUT_FILE = PROJECT_ROOT / "data" / "candles" / "BTCUSD_30m_candlestick.csv"


def refresh_candlesticks():

    print("Refreshing GROHM candlestick patterns...")

    df = pd.read_csv(INPUT_FILE)

    if df.empty:
        raise ValueError("Market dataset is empty.")

    result = identify_candlestick_patterns(df)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False)

    print("Candlestick patterns refreshed successfully!")
    print("Output:", OUTPUT_FILE)
    print("Total rows:", len(result))
    print("Latest pattern:", result.iloc[-1]["Pattern"])
    print("Latest signal:", result.iloc[-1]["Pattern_Signal"])


if __name__ == "__main__":
    refresh_candlesticks()