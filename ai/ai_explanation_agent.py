
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

SIGNAL_FILE = BASE_DIR / "data/candles/BTCUSD_30m_ai_signal.csv"
REGIME_FILE = BASE_DIR / "data/candles/BTCUSD_30m_market_regime.csv"
ANOMALY_FILE = BASE_DIR / "data/candles/BTCUSD_30m_anomalies.csv"

OUTPUT_FILE = BASE_DIR / "data/candles/BTCUSD_30m_ai_explanation.csv"


def run_explanation():

    signal = pd.read_csv(SIGNAL_FILE).iloc[-1]
    regime = pd.read_csv(REGIME_FILE).iloc[-1]
    anomalies = pd.read_csv(ANOMALY_FILE)

    reasons = []

    if signal["Predicted_Price"] > signal["Current_Price"]:
        reasons.append("Predicted price is above current price.")

    elif signal["Predicted_Price"] < signal["Current_Price"]:
        reasons.append("Predicted price is below current price.")

    if regime["Market_Regime"] == "TRENDING_UP":
        reasons.append("EMA 20 is above EMA 50.")

    elif regime["Market_Regime"] == "TRENDING_DOWN":
        reasons.append("EMA 20 is below EMA 50.")

    elif regime["Market_Regime"] == "SIDEWAYS":
        reasons.append("Market is moving sideways.")

    elif regime["Market_Regime"] == "HIGH_VOLATILITY":
        reasons.append("Market volatility is elevated.")

    if anomalies.iloc[-1]["Anomaly_Status"] == "ANOMALY":
        reasons.append("Latest candle has unusual market behaviour.")
    else:
        reasons.append("Latest candle is classified as normal.")

    result = pd.DataFrame([{
        "AI_Signal": signal["AI_Signal"],
        "Market_Regime": regime["Market_Regime"],
        "Explanation": " ".join(reasons)
    }])

    result.to_csv(OUTPUT_FILE, index=False)

    print("\nGROHM AI EXPLANATION")
    print(result.to_string(index=False))
    print("\nSaved:", OUTPUT_FILE)


if __name__ == "__main__":
    run_explanation()
