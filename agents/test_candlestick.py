
import pandas as pd

from candlestick_agent import (
    identify_candlestick_patterns,
    save_candlestick_data
)


if __name__ == "__main__":

    input_file = "data/candles/BTCUSD_30m_validated.csv"

    df = pd.read_csv(input_file)

    result = identify_candlestick_patterns(df)

    save_candlestick_data(
        result,
        symbol="BTCUSD",
        resolution="30m"
    )

    print("\nLatest Candlestick Results:")

    print(
        result[
            ["open", "high", "low", "close",
             "Pattern", "Pattern_Signal"]
        ].tail(15)
    )

    print("\nPattern Summary:")
    print(result["Pattern"].value_counts())

    print("\nDataset Shape:")
    print(result.shape)
