import pandas as pd
def calculate_indicators(df):
    df = df.copy()

    # Convert price columns to numeric values
    for column in ["open", "high", "low", "close", "volume"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Exponential Moving Averages
    df["EMA_20"] = df["close"].ewm(
        span=20, adjust=False, min_periods=20
    ).mean()

    df["EMA_50"] = df["close"].ewm(
        span=50, adjust=False, min_periods=50
    ).mean()

    df["EMA_200"] = df["close"].ewm(
        span=200, adjust=False, min_periods=200
    ).mean()

    # RSI
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(
        alpha=1/14, adjust=False, min_periods=14
    ).mean()

    avg_loss = loss.ewm(
        alpha=1/14, adjust=False, min_periods=14
    ).mean()

    rs = avg_gain / avg_loss
    df["RSI_14"] = 100 - (100 / (1 + rs))

    df.loc[(avg_loss == 0) & (avg_gain > 0), "RSI_14"] = 100
    df.loc[(avg_gain == 0) & (avg_loss > 0), "RSI_14"] = 0

    # MACD
    ema_12 = df["close"].ewm(span=12, adjust=False).mean()
    ema_26 = df["close"].ewm(span=26, adjust=False).mean()

    df["MACD"] = ema_12 - ema_26
    df["MACD_Signal"] = df["MACD"].ewm(
        span=9, adjust=False
    ).mean()
    df["MACD_Histogram"] = df["MACD"] - df["MACD_Signal"]

    # ATR
    previous_close = df["close"].shift(1)

    true_range = pd.concat(
        [
            df["high"] - df["low"],
            (df["high"] - previous_close).abs(),
            (df["low"] - previous_close).abs()
        ],
        axis=1
    ).max(axis=1)

    df["ATR_14"] = true_range.ewm(
        alpha=1/14, adjust=False, min_periods=14
    ).mean()
    df["Volume_SMA_20"] = df["volume"].rolling(window=20).mean()
    return df


def save_indicator_data(df, symbol="BTCUSD", resolution="30m"):
    from pathlib import Path

    output_folder = Path("data/candles")
    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = output_folder / f"{symbol}_{resolution}_indicators.csv"
    df.to_csv(output_file, index=False)

    print(f"Indicator data saved to: {output_file}")

