
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = BASE_DIR / "data/candles/BTCUSD_30m_indicators.csv"
OUTPUT_FILE = BASE_DIR / "data/candles/BTCUSD_30m_market_regime.csv"


def run_market_regime():

    df = pd.read_csv(INPUT_FILE)

    latest = df.dropna(
        subset=["close", "EMA_20", "EMA_50", "ATR_14"]
    ).iloc[-1]

    volatility = latest["ATR_14"] / latest["close"] * 100

    if volatility >= 1.0:
        regime = "HIGH_VOLATILITY"

    elif latest["EMA_20"] > latest["EMA_50"]:
        regime = "TRENDING_UP"

    elif latest["EMA_20"] < latest["EMA_50"]:
        regime = "TRENDING_DOWN"

    else:
        regime = "SIDEWAYS"

    result = pd.DataFrame([{
        "Current_Price": latest["close"],
        "EMA_20": latest["EMA_20"],
        "EMA_50": latest["EMA_50"],
        "Volatility_Percent": volatility,
        "Market_Regime": regime
    }])

    result.to_csv(OUTPUT_FILE, index=False)

    print("\nAI MARKET REGIME")
    print(result.to_string(index=False))
    print("\nSaved:", OUTPUT_FILE)


if __name__ == "__main__":
    run_market_regime()
