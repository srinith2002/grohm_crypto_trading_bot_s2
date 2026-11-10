
from pathlib import Path
import pandas as pd


class TechnicalAnalysisAgent:

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.data_file = (
            self.project_root
            / "data"
            / "candles"
            / "BTCUSD_30m_indicators.csv"
        )

    def analyze_market(self):

        if not self.data_file.exists():
            raise FileNotFoundError(
                f"Indicator file not found: {self.data_file}"
            )

        df = pd.read_csv(self.data_file)

        if df.empty:
            raise ValueError("Indicator data is empty.")

        required_columns = [
            "EMA_20",
            "EMA_50",
            "EMA_200",
            "RSI_14",
            "MACD",
            "MACD_Signal",
            "MACD_Histogram",
            "ATR_14"
        ]

        missing = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing indicator columns: {missing}"
            )

        latest = df.iloc[-1]

        def safe_value(column):
            value = latest[column]
            return None if pd.isna(value) else float(value)

        ema_20 = safe_value("EMA_20")
        ema_50 = safe_value("EMA_50")
        rsi = safe_value("RSI_14")
        macd = safe_value("MACD")
        macd_signal = safe_value("MACD_Signal")
        histogram = safe_value("MACD_Histogram")

        if ema_20 is not None and ema_50 is not None:
            trend = (
                "BULLISH" if ema_20 > ema_50
                else "BEARISH" if ema_20 < ema_50
                else "NEUTRAL"
            )
        else:
            trend = "UNAVAILABLE"

        if rsi is None:
            momentum = "UNAVAILABLE"
        elif rsi >= 70:
            momentum = "HIGH"
        elif rsi <= 30:
            momentum = "LOW"
        else:
            momentum = "NORMAL"

        if macd is None or macd_signal is None:
            macd_condition = "UNAVAILABLE"
        elif macd > macd_signal:
            macd_condition = "BULLISH"
        elif macd < macd_signal:
            macd_condition = "BEARISH"
        else:
            macd_condition = "NEUTRAL"

        return {
            "agent": "Technical Analysis Agent",
            "status": "SUCCESS",
            "latest_time": str(latest["time"]),
            "close": float(latest["close"]),
            "indicators": {
                "EMA_20": ema_20,
                "EMA_50": ema_50,
                "EMA_200": safe_value("EMA_200"),
                "RSI_14": rsi,
                "MACD": macd,
                "MACD_Signal": macd_signal,
                "MACD_Histogram": histogram,
                "ATR_14": safe_value("ATR_14")
            },
            "analysis": {
                "trend": trend,
                "momentum": momentum,
                "macd_condition": macd_condition
            }
        }
