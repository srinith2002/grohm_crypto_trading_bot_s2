
import requests
import pandas as pd
import time
from pathlib import Path

BASE_URL = "https://api.india.delta.exchange"

DATA_FOLDER = Path("data/candles")
DATA_FOLDER.mkdir(parents=True, exist_ok=True)


def fetch_market_data(symbol, resolution="30m", limit=100):

    print(f"Fetching market data for {symbol}...")

    interval_seconds = {
        "1m": 60,
        "5m": 300,
        "15m": 900,
        "30m": 1800,
        "1h": 3600,
        "4h": 14400,
        "1d": 86400
    }

    if resolution not in interval_seconds:
        raise ValueError("Unsupported resolution")

    end_time = int(time.time())
    start_time = end_time - (
        interval_seconds[resolution] * limit
    )

    url = f"{BASE_URL}/v2/history/candles"

    params = {
        "symbol": symbol,
        "resolution": resolution,
        "start": start_time,
        "end": end_time
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    result = response.json()

    if not result.get("success"):
        raise RuntimeError(f"API error: {result}")

    candles = result.get("result", [])

    if not candles:
        raise ValueError(f"No candle data received for {symbol}")

    df = pd.DataFrame(candles)

    required_columns = [
        "time", "open", "high", "low", "close", "volume"
    ]

    if not all(col in df.columns for col in required_columns):
        raise ValueError("Unexpected candle data format")

    df = df[required_columns].copy()

    df["time"] = pd.to_datetime(
        df["time"], unit="s", utc=True
    )

    df = df.sort_values("time")
    df = df.drop_duplicates(subset=["time"])
    df = df.reset_index(drop=True)

    file_path = DATA_FOLDER / f"{symbol}_{resolution}.csv"

    df.to_csv(file_path, index=False)

    print(f"Symbol: {symbol}")
    print(f"Total candles: {len(df)}")
    print(f"Saved to: {file_path}")

    return df

