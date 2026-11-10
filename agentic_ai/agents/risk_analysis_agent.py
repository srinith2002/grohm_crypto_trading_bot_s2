
from pathlib import Path
import pandas as pd


class RiskAnalysisAgent:

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.data_file = (
            self.project_root
            / "data"
            / "candles"
            / "BTCUSD_30m_risk_results.csv"
        )

    def analyze_risk(self):

        if not self.data_file.exists():
            raise FileNotFoundError(
                f"Risk results file not found: {self.data_file}"
            )

        df = pd.read_csv(self.data_file)

        if df.empty:
            raise ValueError("Risk results file is empty.")

        required_columns = [
            "time",
            "signal",
            "status",
            "reason",
            "stop_loss",
            "take_profit",
            "position_size",
            "risk_amount",
            "potential_reward"
        ]

        missing = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing risk columns: {missing}"
            )

        latest = df.iloc[-1]

        def safe_value(column):
            value = latest[column]
            return None if pd.isna(value) else float(value)

        return {
            "agent": "Risk Analysis Agent",
            "status": "SUCCESS",
            "latest_time": str(latest["time"]),
            "signal": str(latest["signal"]),
            "risk_status": str(latest["status"]),
            "reason": str(latest["reason"]),
            "risk_details": {
                "stop_loss": safe_value("stop_loss"),
                "take_profit": safe_value("take_profit"),
                "position_size": safe_value("position_size"),
                "risk_amount": safe_value("risk_amount"),
                "potential_reward": safe_value("potential_reward")
            }
        }
