
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "candles"

files = {
    "Linear Regression": "BTCUSD_30m_linear_regression_results.csv",
    "Random Forest": "BTCUSD_30m_random_forest_results.csv",
    "XGBoost": "BTCUSD_30m_xgboost_results.csv",
    "Ensemble": "BTCUSD_30m_ensemble_results.csv"
}

print("Starting Model Comparison Agent...")

all_results = []

for model_name, filename in files.items():

    file_path = DATA_DIR / filename

    if not file_path.exists():
        print(f"Missing file: {filename}")
        continue

    df = pd.read_csv(file_path)

    actual = df["Actual_Close"]
    prediction_column = (
        "Ensemble_Prediction"
        if model_name == "Ensemble"
        else "Predicted_Close"
    )

    predicted = df[prediction_column]

    if len(actual) != len(predicted):
        print(f"Skipping {model_name}: row mismatch")
        continue

    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    r2 = r2_score(actual, predicted)

    all_results.append({
        "Model": model_name,
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "R2_Score": round(r2, 4)
    })

if not all_results:
    raise ValueError("No model results available.")

results = pd.DataFrame(all_results)

results = results.sort_values("MAE")

print("\nModel Comparison Results:")
print(results.to_string(index=False))

output_file = DATA_DIR / "BTCUSD_30m_model_comparison.csv"

results.to_csv(output_file, index=False)

print("\nBest model by MAE:", results.iloc[0]["Model"])
print("Saved:", output_file)
