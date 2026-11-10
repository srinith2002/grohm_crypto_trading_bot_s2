
import pandas as pd
from pathlib import Path


DATA_FOLDER = Path("data/candles")


def validate_market_data(df, symbol="BTCUSD"):

    print(f"\nValidating market data for {symbol}...")

    required_columns = [
        "time", "open", "high",
        "low", "close", "volume"
    ]

    # 1. Check required columns
    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    df = df[required_columns].copy()

    original_rows = len(df)

    # 2. Convert price and volume columns to numeric
    numeric_columns = [
        "open", "high", "low", "close", "volume"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(
            df[col], errors="coerce"
        )

    # 3. Convert timestamps
    df["time"] = pd.to_datetime(
        df["time"], utc=True, errors="coerce"
    )

    # 4. Remove missing values
    df = df.dropna(subset=required_columns)

    # 5. Remove duplicate candles
    df = df.drop_duplicates(
        subset=["time"], keep="last"
    )

    # 6. Check positive prices and non-negative volume
    valid_prices = (
        (df[numeric_columns[:4]] > 0).all(axis=1)
    )

    valid_volume = df["volume"] >= 0

    # 7. Check OHLC price consistency
    valid_high = df["high"] >= df[
        ["open", "close", "low"]
    ].max(axis=1)

    valid_low = df["low"] <= df[
        ["open", "close", "high"]
    ].min(axis=1)

    valid_rows = (
        valid_prices
        & valid_volume
        & valid_high
        & valid_low
    )

    df = df[valid_rows].copy()

    # 8. Sort candles by time
    df = df.sort_values("time")
    df = df.reset_index(drop=True)

    if df.empty:
        raise ValueError(
            "No valid market candles remain."
        )

    # 9. Save validated data
    DATA_FOLDER.mkdir(
        parents=True, exist_ok=True
    )

    file_path = DATA_FOLDER / (
        f"{symbol}_30m_validated.csv"
    )

    df.to_csv(file_path, index=False)

    # 10. Display validation report
    print("\n----- VALIDATION REPORT -----")

    print("Original rows:", original_rows)
    print("Valid rows:", len(df))
    print("Rejected rows:", original_rows - len(df))
    print("Missing values:", df.isnull().sum().sum())
    print("Duplicate timestamps:", df["time"].duplicated().sum())

    print("Data validation completed.")
    print("Saved file:", file_path)

    return df

