import pandas as pd
def identify_candlestick_patterns(df):
    df = df.copy()

    required_columns = ["open", "high", "low", "close"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["Pattern"] = "No Pattern"
    df["Pattern_Signal"] = "NEUTRAL"

    for i in range(1, len(df)):
        current = df.iloc[i]
        previous = df.iloc[i - 1]

        open_price = current["open"]
        high = current["high"]
        low = current["low"]
        close = current["close"]

        previous_open = previous["open"]
        previous_close = previous["close"]

        candle_range = high - low

        if candle_range <= 0:
            continue

        body = abs(close - open_price)
        upper_shadow = high - max(open_price, close)
        lower_shadow = min(open_price, close) - low

        # Bullish Engulfing
        if (
            previous_close < previous_open
            and close > open_price
            and open_price <= previous_close
            and close >= previous_open
        ):
            df.loc[df.index[i], "Pattern"] = "Bullish Engulfing"
            df.loc[df.index[i], "Pattern_Signal"] = "BULLISH"

        # Bearish Engulfing
        elif (
            previous_close > previous_open
            and close < open_price
            and open_price >= previous_close
            and close <= previous_open
        ):
            df.loc[df.index[i], "Pattern"] = "Bearish Engulfing"
            df.loc[df.index[i], "Pattern_Signal"] = "BEARISH"

        # Doji
        elif body <= candle_range * 0.10:
            df.loc[df.index[i], "Pattern"] = "Doji"
            df.loc[df.index[i], "Pattern_Signal"] = "NEUTRAL"

        # Hammer
        elif (
            lower_shadow >= body * 2
            and upper_shadow <= body
            and body > 0
        ):
            df.loc[df.index[i], "Pattern"] = "Hammer"
            df.loc[df.index[i], "Pattern_Signal"] = "BULLISH"

        # Shooting Star
        elif (
            upper_shadow >= body * 2
            and lower_shadow <= body
            and body > 0
        ):
            df.loc[df.index[i], "Pattern"] = "Shooting Star"
            df.loc[df.index[i], "Pattern_Signal"] = "BEARISH"

    return df


def save_candlestick_data(df, symbol="BTCUSD", resolution="30m"):
    from pathlib import Path

    output_folder = Path("data/candles")
    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = (
        output_folder /
        f"{symbol}_{resolution}_candlestick.csv"
    )

    df.to_csv(output_file, index=False)

    print(f"Candlestick data saved to: {output_file}")
