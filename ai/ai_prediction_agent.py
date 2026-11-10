
import pandas as pd
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_FILE = BASE_DIR / "data/candles/BTCUSD_30m_indicators.csv"
MODEL_DIR = BASE_DIR / "models"
OUTPUT_FILE = BASE_DIR / "data/candles/BTCUSD_30m_ai_prediction.csv"

FEATURES = [
    "open", "high", "low", "close", "volume",
    "EMA_20", "EMA_50", "RSI_14",
    "MACD", "MACD_Signal", "ATR_14"
]

def run_prediction():

    df = pd.read_csv(DATA_FILE)
    df = df.dropna(subset=FEATURES)

    latest = df[FEATURES].iloc[[-1]]

    models = {
        "Linear_Regression": "linear_regression.pkl",
        "Random_Forest": "random_forest.pkl",
        "XGBoost": "xgboost_model.pkl"
    }

    predictions = {}

    for name, filename in models.items():
        model = joblib.load(MODEL_DIR / filename)
        predictions[name] = float(model.predict(latest)[0])

    ensemble = sum(predictions.values()) / len(predictions)

    result = pd.DataFrame([{
        **predictions,
        "Ensemble_Prediction": ensemble,
        "Current_Close": float(latest["close"].iloc[0])
    }])

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False)

    print("\nGROHM AI PREDICTION")
    print(result.to_string(index=False))
    print("\nSaved:", OUTPUT_FILE)


if __name__ == "__main__":
    run_prediction()
