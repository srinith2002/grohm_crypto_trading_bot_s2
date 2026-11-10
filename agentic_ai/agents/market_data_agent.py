
from pathlib import Path
import pandas as pd


class MarketDataAgent:

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.data_file = (
            self.project_root
            / "data"
            / "candles"
            / "BTCUSD_30m.csv"
        )

    def load_market_data(self):

        if not self.data_file.exists():
            raise FileNotFoundError(
                f"Market data file not found: {self.data_file}"
            )

        df = pd.read_csv(self.data_file)

        if df.empty:
            raise ValueError("Market data file is empty.")

        required_columns = [
            "time", "open", "high",
            "low", "close", "volume"
        ]

        missing = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing market columns: {missing}"
            )

        latest = df.iloc[-1]

        return {
            "agent": "Market Data Agent",
            "status": "SUCCESS",
            "symbol": "BTCUSD",
            "timeframe": "30m",
            "total_candles": len(df),
            "latest_time": str(latest["time"]),
            "latest_open": float(latest["open"]),
            "latest_high": float(latest["high"]),
            "latest_low": float(latest["low"]),
            "latest_close": float(latest["close"]),
            "latest_volume": float(latest["volume"])
        }

