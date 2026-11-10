
import pandas as pd

from indicator_agent import (
    calculate_indicators,
    save_indicator_data
)


if __name__ == "__main__":

    input_file = (
        "data/candles/BTCUSD_30m_validated.csv"
    )

    df = pd.read_csv(input_file)

    # Calculate indicators
    result = calculate_indicators(df)

    # Save results
    save_indicator_data(
        result,
        symbol="BTCUSD",
        resolution="30m"
    )

    print("\nLatest Indicator Results:")

    columns = [
        "close",
        "EMA_20",
        "EMA_50",
        "EMA_200",
        "RSI_14",
        "MACD",
        "MACD_Signal",
        "ATR_14"
    ]

    print(result[columns].tail(10))

    print("\nIndicator Dataset Shape:")
    print(result.shape)
