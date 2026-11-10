
from pathlib import Path
import pandas as pd

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "candles"

INPUT_FILE = DATA_DIR / "BTCUSD_30m_indicators.csv"
OUTPUT_FILE = DATA_DIR / "BTCUSD_30m_ml_dataset.csv"

# Load indicator data
if not INPUT_FILE.exists():
    raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

df = pd.read_csv(INPUT_FILE)

# Features used by the ML models
features = [
    "open",
    "high",
    "low",
    "close",
    "volume",
    "EMA_20",
    "EMA_50",
    "RSI_14",
    "MACD",
    "MACD_Signal",
    "ATR_14"
]

# Check required columns
missing = [col for col in features if col not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

# Create next-candle closing price target
df["Target_Next_Close"] = df["close"].shift(-1)

# Keep only features and target
dataset = df[features + ["Target_Next_Close"]].copy()

# Convert values to numeric and remove invalid rows
for col in dataset.columns:
    dataset[col] = pd.to_numeric(dataset[col], errors="coerce")

dataset = dataset.dropna().reset_index(drop=True)

if dataset.empty:
    raise ValueError("ML dataset is empty. Check the input indicator data.")

# Save dataset
dataset.to_csv(OUTPUT_FILE, index=False)

print("ML dataset created successfully!")
print("Saved at:", OUTPUT_FILE)
print("Total records:", len(dataset))
print("Features:", features)
print("Target: Target_Next_Close")
print("\nDataset preview:")
print(dataset.head())
