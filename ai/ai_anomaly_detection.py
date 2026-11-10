
import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = BASE_DIR / "data/candles/BTCUSD_30m_indicators.csv"
OUTPUT_FILE = BASE_DIR / "data/candles/BTCUSD_30m_anomalies.csv"


def run_anomaly_detection():

    df = pd.read_csv(INPUT_FILE)

    features = ["close", "volume", "ATR_14"]

    data = df.dropna(subset=features).copy()

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    predictions = model.fit_predict(data[features])

    data["Anomaly_Status"] = [
        "ANOMALY" if value == -1 else "NORMAL"
        for value in predictions
    ]

    data.to_csv(OUTPUT_FILE, index=False)

    print("\nAI ANOMALY DETECTION")
    print(data[["close", "volume", "ATR_14", "Anomaly_Status"]].tail(10))

    print("\nTotal anomalies:",
          (data["Anomaly_Status"] == "ANOMALY").sum())

    print("\nSaved:", OUTPUT_FILE)


if __name__ == "__main__":
    run_anomaly_detection()
