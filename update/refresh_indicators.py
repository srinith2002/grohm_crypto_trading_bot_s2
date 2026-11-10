
import pandas as pd
from pathlib import Path

from agents.indicator_agent import (
    calculate_indicators,
    save_indicator_data
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT / "data" / "candles" / "BTCUSD_30m.csv"
)


def refresh_indicators():

    print("Refreshing GROHM technical indicators...")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(INPUT_FILE)

    df = pd.read_csv(INPUT_FILE)

    if df.empty:
        raise ValueError("Market dataset is empty.")

    result = calculate_indicators(df)

    output_file = (
        PROJECT_ROOT
        / "data"
        / "candles"
        / "BTCUSD_30m_indicators.csv"
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)

    result.to_csv(output_file, index=False)

    print("Indicators refreshed successfully!")
    print("Output:", output_file)
    print("Total rows:", len(result))
    print("Latest close:", result.iloc[-1]["close"])
    print("Latest EMA 20:", result.iloc[-1]["EMA_20"])
    print("Latest RSI 14:", result.iloc[-1]["RSI_14"])


if __name__ == "__main__":
    refresh_indicators()
