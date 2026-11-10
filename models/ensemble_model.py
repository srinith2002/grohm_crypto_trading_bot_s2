
import pandas as pd
import numpy as np
import joblib

from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_FILE = BASE_DIR / "data" / "candles" / "BTCUSD_30m_indicators.csv"
MODEL_DIR = BASE_DIR / "models"
OUTPUT_DIR = BASE_DIR / "data" / "candles"

features = [
    "open", "high", "low", "close", "volume",
    "EMA_20", "EMA_50", "RSI_14",
    "MACD", "MACD_Signal", "ATR_14"
]

print("Loading historical data...")

df = pd.read_csv(DATA_FILE)

if "time" in df.columns:
    df = df.sort_values("time")

df["Target_Next_Close"] = df["close"].shift(-1)

df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna(subset=features + ["Target_Next_Close"])

X = df[features]
y = df["Target_Next_Close"]

split_index = int(len(df) * 0.80)

X_test = X.iloc[split_index:]
y_test = y.iloc[split_index:]

if X_test.empty:
    raise ValueError("Not enough test data.")

print("Loading trained models...")

linear_model = joblib.load(
    MODEL_DIR / "linear_regression.pkl"
)

forest_model = joblib.load(
    MODEL_DIR / "random_forest.pkl"
)

xgboost_model = joblib.load(
    MODEL_DIR / "xgboost_model.pkl"
)

print("Generating predictions...")

linear_predictions = linear_model.predict(X_test)
forest_predictions = forest_model.predict(X_test)
xgboost_predictions = xgboost_model.predict(X_test)

# Average all three predictions
ensemble_predictions = (
    linear_predictions +
    forest_predictions +
    xgboost_predictions
) / 3

# Simple baseline: next close equals current close
baseline_predictions = X_test["close"].values

print("\nEnsemble Model Results")
print("----------------------")

models = {
    "Linear Regression": linear_predictions,
    "Random Forest": forest_predictions,
    "XGBoost": xgboost_predictions,
    "Ensemble": ensemble_predictions,
    "Baseline": baseline_predictions
}

for name, predictions in models.items():
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    print(f"\n{name}")
    print("MAE:", round(mae, 2))
    print("RMSE:", round(rmse, 2))
    print("R2 Score:", round(r2, 4))

# Save predictions
results = pd.DataFrame({
    "Actual_Close": y_test.values,
    "Linear_Regression": linear_predictions,
    "Random_Forest": forest_predictions,
    "XGBoost": xgboost_predictions,
    "Ensemble_Prediction": ensemble_predictions,
    "Baseline": baseline_predictions
})

results.to_csv(
    OUTPUT_DIR / "BTCUSD_30m_ensemble_results.csv",
    index=False
)

print("\nEnsemble predictions saved successfully!")
print("File: data/candles/BTCUSD_30m_ensemble_results.csv")
