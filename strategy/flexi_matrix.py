
def calculate_flexi_matrix(row):

    scores = {
        "trend": 0,
        "candlestick": 0,
        "momentum": 0,
        "market_structure": 0,
        "volume": 0,
        "volatility": 0,
        "multi_timeframe": 0
    }

    # 1. Trend Analysis (20)
    if row["close"] > row["EMA_20"] > row["EMA_50"]:
        scores["trend"] = 20
    elif row["close"] < row["EMA_20"] < row["EMA_50"]:
        scores["trend"] = -20

    # 2. Candlestick Analysis (20)
    pattern = row["Pattern"]

    if pattern in ["Bullish Engulfing", "Hammer"]:
        scores["candlestick"] = 20
    elif pattern in ["Bearish Engulfing", "Shooting Star"]:
        scores["candlestick"] = -20
    else:
        scores["candlestick"] = 0

    # 3. Momentum Analysis (15)
    if row["RSI_14"] > 55 and row["MACD"] > row["MACD_Signal"]:
        scores["momentum"] = 15
    elif row["RSI_14"] < 45 and row["MACD"] < row["MACD_Signal"]:
        scores["momentum"] = -15

    # 4. Market Structure (15)
    if row["close"] > row["EMA_50"]:
        scores["market_structure"] = 15
    elif row["close"] < row["EMA_50"]:
        scores["market_structure"] = -15

    # 5. Volume Analysis (10)
    if row["volume"] > row["Volume_SMA_20"]:
        scores["volume"] = 10

    # 6. Volatility Analysis (10)
    if row["ATR_14"] > 0:
        scores["volatility"] = 10

    # 7. Multi-Timeframe Analysis (10)
    # Placeholder until higher timeframe data is added.
    scores["multi_timeframe"] = 0

    total_score = sum(scores.values())

    if total_score >= 70:
        signal = "LONG_CANDIDATE"
    elif total_score <= -70:
        signal = "SHORT_CANDIDATE"
    else:
        signal = "HOLD"

    return {
        **scores,
        "total_score": total_score,
        "signal": signal
    }
