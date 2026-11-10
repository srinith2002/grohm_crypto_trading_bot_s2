
from pathlib import Path
import pandas as pd


class MLPredictionAgent:

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.data_file = (
            self.project_root
            / "data"
            / "candles"
            / "BTCUSD_30m_ensemble_results.csv"
        )

    def analyze_prediction(self):

        if not self.data_file.exists():
            raise FileNotFoundError(
                f"Ensemble results not found: {self.data_file}"
            )

        df = pd.read_csv(self.data_file)

        if df.empty:
            raise ValueError("Ensemble results are empty.")

        required_columns = [
            "Actual_Close",
            "Linear_Regression",
            "Random_Forest",
            "XGBoost",
            "Ensemble_Prediction",
            "Baseline"
        ]

        missing = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing ML columns: {missing}"
            )

        latest = df.iloc[-1]

        actual = float(latest["Actual_Close"])
        predicted = float(latest["Ensemble_Prediction"])

        difference = predicted - actual

        prediction_direction = (
            "ABOVE_ACTUAL" if difference > 0
            else "BELOW_ACTUAL" if difference < 0
            else "EQUAL_TO_ACTUAL"
        )

        return {
            "agent": "ML Prediction Agent",
            "status": "SUCCESS",
            "actual_close": actual,
            "ensemble_prediction": predicted,
            "prediction_difference": round(difference, 4),
            "prediction_direction": prediction_direction,
            "model_predictions": {
                "Linear_Regression": float(latest["Linear_Regression"]),
                "Random_Forest": float(latest["Random_Forest"]),
                "XGBoost": float(latest["XGBoost"])
            }
        }
