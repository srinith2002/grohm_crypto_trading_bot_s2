
import time
import requests
import pandas as pd
from pathlib import Path

# Main project folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# One common dataset for all GROHM modules
CSV_PATH = (
    PROJECT_ROOT / "data" / "candles" / "BTCUSD_30m.csv"
)


def update_market_data():

    print("Fetching latest BTCUSD data...")

    # Today's midnight in IST, converted to UTC.
    # This excludes today's candles and keeps data through yesterday.
    cutoff = (
        pd.Timestamp.now(tz="Asia/Kolkata")
        .normalize()
        .tz_convert("UTC")
    )

    end_time = int(cutoff.timestamp())
    start_time = end_time - (100 * 1800)

    url = "https://api.india.delta.exchange/v2/history/candles"

    params = {
        "resolution": "30m",
        "symbol": "BTCUSD",
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
        raise RuntimeError(result)

    df = pd.DataFrame(result["result"])

    if df.empty:
        raise ValueError("No market data received")

    df = df[
        ["time", "open", "high", "low", "close", "volume"]
    ]

    df["time"] = pd.to_datetime(
        df["time"], unit="s", utc=True
    )

    # Keep only completed historical candles through yesterday.
    df = df[df["time"] < cutoff]

    df = df.sort_values("time")
    df = df.drop_duplicates(subset=["time"])
    df = df.reset_index(drop=True)

    if df.empty:
        raise ValueError("No completed candles received.")

    CSV_PATH.parent.mkdir(
        parents=True, exist_ok=True
    )

    df.to_csv(CSV_PATH, index=False)

    print("Market data updated successfully!")
    print("Saved location:", CSV_PATH)
    print("Total candles:", len(df))
    print("Latest candle:", df["time"].iloc[-1])


if __name__ == "__main__":
    update_market_data()

