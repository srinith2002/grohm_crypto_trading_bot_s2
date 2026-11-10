
from pathlib import Path
import pandas as pd


class StrategyAgent:

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.data_file = (
            self.project_root
            / "data"
            / "candles"
            / "BTCUSD_30m_flexi_matrix.csv"
        )

    def analyze_strategy(self):

        if not self.data_file.exists():
            raise FileNotFoundError(
                f"Flexi Matrix file not found: {self.data_file}"
            )

        df = pd.read_csv(self.data_file)

        if df.empty:
            raise ValueError("Flexi Matrix data is empty.")

        required_columns = [
            "time",
            "total_score",
            "signal",
            "trend",
            "candlestick",
            "momentum",
            "market_structure",
            "volatility"
        ]

        missing = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing strategy columns: {missing}"
            )

        latest = df.iloc[-1]

        return {
            "agent": "Strategy Agent",
            "status": "SUCCESS",
            "latest_time": str(latest["time"]),
            "total_score": float(latest["total_score"]),
            "signal": str(latest["signal"]),
            "strategy_scores": {
                "trend": float(latest["trend"]),
                "candlestick": float(latest["candlestick"]),
                "momentum": float(latest["momentum"]),
                "market_structure": float(latest["market_structure"]),
                "volatility": float(latest["volatility"])
            }
        }
