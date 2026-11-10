
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

PREDICTION_FILE = (
    BASE_DIR / "data/candles/BTCUSD_30m_ai_prediction.csv"
)

INDICATOR_FILE = (
    BASE_DIR / "data/candles/BTCUSD_30m_indicators.csv"
)

OUTPUT_FILE = (
    BASE_DIR / "data/candles/BTCUSD_30m_ai_signal.csv"
)


def run_ai_signal():

    prediction = pd.read_csv(PREDICTION_FILE)
    indicators = pd.read_csv(INDICATOR_FILE)

    latest = indicators.dropna(
        subset=["close", "EMA_20", "EMA_50", "RSI_14", "MACD"]
    ).iloc[-1]

    predicted_price = prediction["Ensemble_Prediction"].iloc[-1]
    current_price = latest["close"]

    score = 0

    if predicted_price > current_price:
        score += 1

    if latest["EMA_20"] > latest["EMA_50"]:
        score += 1

    if latest["RSI_14"] > 50:
        score += 1

    if latest["MACD"] > 0:
        score += 1

    if score >= 3:
        signal = "BULLISH"
    elif score <= 1:
        signal = "BEARISH"
    else:
        signal = "NEUTRAL"

    result = pd.DataFrame([{
        "Current_Price": current_price,
        "Predicted_Price": predicted_price,
        "Score": score,
        "AI_Signal": signal
    }])

    result.to_csv(OUTPUT_FILE, index=False)

    print("\nGROHM AI SIGNAL")
    print(result.to_string(index=False))
    print("\nSaved:", OUTPUT_FILE)


if __name__ == "__main__":
    run_ai_signal()
