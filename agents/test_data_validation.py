
import pandas as pd

from data_validation_agent import validate_market_data


if __name__ == "__main__":

    # Read collected BTC candles
    file_path = "data/candles/BTCUSD_30m.csv"

    df = pd.read_csv(file_path)

    # Validate market data
    clean_df = validate_market_data(
        df,
        symbol="BTCUSD"
    )

    print("\nLatest Validated Candles:")
    print(clean_df.tail())

    print("\nFinal Dataset Shape:")
    print(clean_df.shape)

