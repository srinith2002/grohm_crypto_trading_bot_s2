import pandas as pd
from pathlib import Path

from strategy.flexi_matrix import calculate_flexi_matrix

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CANDLE_FILE = PROJECT_ROOT / "data" / "candles" / "BTCUSD_30m.csv"

INDICATOR_FILE = PROJECT_ROOT / "data" / "candles" / "BTCUSD_30m_indicators.csv"

PATTERN_FILE = PROJECT_ROOT / "data" / "candles" / "BTCUSD_30m_candlestick.csv"

OUTPUT_FILE = PROJECT_ROOT / "data" / "candles" / "BTCUSD_30m_flexi_matrix.csv"


def refresh_flexi_matrix():

    print("Refreshing GROHM Flexi Matrix...")

    candles = pd.read_csv(CANDLE_FILE)
    indicators = pd.read_csv(INDICATOR_FILE)
    patterns = pd.read_csv(PATTERN_FILE)

    if candles.empty or indicators.empty or patterns.empty:
        raise ValueError("One or more input datasets are empty.")

    # Combine refreshed datasets by timestamp.
    df = candles.merge(
        indicators.drop(
            columns=["open", "high", "low", "close", "volume"],
            errors="ignore"
        ),
        on="time",
        how="inner"
    )

    df = df.merge(
        patterns[["time", "Pattern", "Pattern_Signal"]],
        on="time",
        how="inner"
    )

    if df.empty:
        raise ValueError("No matching timestamps across input datasets.")

    # Calculate Flexi Matrix scores.
    results = df.apply(
        calculate_flexi_matrix,
        axis=1,
        result_type="expand"
    )

    final_df = pd.concat([df, results], axis=1)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(OUTPUT_FILE, index=False)

    print("Flexi Matrix refreshed successfully!")
    print("Output:", OUTPUT_FILE)
    print("Total rows:", len(final_df))
    print("Latest score:", final_df.iloc[-1]["total_score"])
    print("Latest signal:", final_df.iloc[-1]["signal"])


if __name__ == "__main__":
    refresh_flexi_matrix()