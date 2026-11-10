
import pandas as pd
from flexi_matrix import calculate_flexi_matrix

if __name__ == "__main__":

    indicator_file = "data/candles/BTCUSD_30m_indicators.csv"
    candlestick_file = "data/candles/BTCUSD_30m_candlestick.csv"

    print("Loading indicator data...")
    indicators = pd.read_csv(indicator_file)

    print("Loading candlestick data...")
    candles = pd.read_csv(candlestick_file)

    # Keep only the candlestick columns needed
    pattern_data = candles[
        ["time", "Pattern", "Pattern_Signal"]
    ]

    # Merge indicator and candlestick data using time
    df = pd.merge(
        indicators,
        pattern_data,
        on="time",
        how="inner"
    )

    print("\nCombined dataset loaded!")
    print("Available columns:", df.columns.tolist())

    # Calculate Flexi Matrix scores
    results = df.apply(calculate_flexi_matrix, axis=1)

    results_df = pd.DataFrame(results.tolist())

    final_df = pd.concat(
        [df.reset_index(drop=True),
         results_df.reset_index(drop=True)],
        axis=1
    )

    print("\nFlexi Matrix Results:")

    print(final_df[[
        "close",
        "EMA_20",
        "EMA_50",
        "RSI_14",
        "Pattern",
        "total_score",
        "signal"
    ]].tail(10))

    output_file = "data/candles/BTCUSD_30m_flexi_matrix.csv"

    final_df.to_csv(output_file, index=False)

    print("\nSaved successfully:", output_file)


