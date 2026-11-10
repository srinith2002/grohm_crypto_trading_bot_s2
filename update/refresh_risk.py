import pandas as pd
from pathlib import Path

from agents.risk_management_agent import evaluate_risk

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT / "data" / "candles" / "BTCUSD_30m_flexi_matrix.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT / "data" / "candles" / "BTCUSD_30m_risk_results.csv"
)


def refresh_risk():

    print("Refreshing GROHM Risk Management...")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(INPUT_FILE)

    df = pd.read_csv(INPUT_FILE)

    if df.empty:
        raise ValueError("Flexi Matrix dataset is empty.")

    results = df.apply(
        evaluate_risk,
        axis=1,
        result_type="expand"
    )

    final_df = pd.concat([df, results], axis=1)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    final_df.to_csv(OUTPUT_FILE, index=False)

    print("Risk Management refreshed successfully!")
    print("Output:", OUTPUT_FILE)
    print("Total rows:", len(final_df))
    print("Latest status:", final_df.iloc[-1]["status"])
    print("Latest reason:", final_df.iloc[-1]["reason"])


if __name__ == "__main__":
    refresh_risk()