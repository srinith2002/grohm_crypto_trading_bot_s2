
import pandas as pd
import numpy as np
import joblib

from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_FILE = BASE_DIR / "data" / "candles" / "BTCUSD_30m_indicators.csv"
MODEL_DIR = BASE_DIR / "models"
OUTPUT_DIR = BASE_DIR / "data" / "candles"

MODEL_DIR.mkdir(exist_ok=True)

print("Loading BTC historical data...")

df = pd.read_csv(DATA_FILE)

features = [
    "open", "high", "low", "close", "volume",
    "EMA_20", "EMA_50", "RSI_14",
    "MACD", "MACD_Signal", "ATR_14"
]

missing = [col for col in features if col not in df.columns]

if missing:
    raise ValueError(f"Missing columns: {missing}")

if "time" in df.columns:
    df = df.sort_values("time")

df["Target_Next_Close"] = df["close"].shift(-1)

df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna(subset=features + ["Target_Next_Close"])

X = df[features]
y = df["Target_Next_Close"]

if len(df) < 20:
    raise ValueError("Not enough valid rows. Collect more historical data.")

# Chronological 80:20 split
split_index = int(len(df) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("Training Random Forest model...")

model = RandomForestRegressor(
    n_estimators=100,
    max_depth=8,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

baseline = X_test["close"].values

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

baseline_mae = mean_absolute_error(y_test, baseline)

print("\nRandom Forest Results")
print("---------------------")
print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))
print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R2 Score:", round(r2, 4))
print("Baseline MAE:", round(baseline_mae, 2))

joblib.dump(model, MODEL_DIR / "random_forest.pkl")

results = pd.DataFrame({
    "Actual_Close": y_test.values,
    "Predicted_Close": predictions,
    "Baseline_Close": baseline
})

results.to_csv(
    OUTPUT_DIR / "BTCUSD_30m_random_forest_results.csv",
    index=False
)

print("\nModel saved: models/random_forest.pkl")
print("Results saved: data/candles/BTCUSD_30m_random_forest_results.csv")
print("\nRandom Forest completed!")
