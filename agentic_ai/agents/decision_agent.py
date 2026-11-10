
class DecisionAgent:

    def decide(
        self,
        market_data,
        technical_analysis,
        strategy_analysis,
        risk_analysis,
        ml_prediction
    ):

        reasons = []

        signal = strategy_analysis.get("signal", "HOLD")
        risk_status = risk_analysis.get("risk_status", "UNKNOWN")

        trend = technical_analysis.get(
            "analysis", {}
        ).get("trend", "UNAVAILABLE")

        macd = technical_analysis.get(
            "analysis", {}
        ).get("macd_condition", "UNAVAILABLE")

        prediction_direction = ml_prediction.get(
            "prediction_direction", "UNAVAILABLE"
        )

        if signal == "HOLD":
            reasons.append("Strategy signal is HOLD.")

        if risk_status != "APPROVED":
            reasons.append("Risk checks are not approved.")

        if trend == "BULLISH" and macd == "BEARISH":
            reasons.append("Technical indicators show mixed conditions.")

        if prediction_direction == "ABOVE_ACTUAL":
            reasons.append(
                "Ensemble prediction is above the recorded actual close."
            )
        elif prediction_direction == "BELOW_ACTUAL":
            reasons.append(
                "Ensemble prediction is below the recorded actual close."
            )

        if risk_status != "APPROVED" or signal == "HOLD":
            decision = "HOLD"
        elif signal in ["LONG_CANDIDATE", "SHORT_CANDIDATE"]:
            decision = "PAPER_REVIEW_REQUIRED"
        else:
            decision = "HOLD"

        return {
            "agent": "Decision Agent",
            "status": "SUCCESS",
            "decision": decision,
            "market_price": market_data.get("latest_close"),
            "strategy_signal": signal,
            "risk_status": risk_status,
            "technical_trend": trend,
            "macd_condition": macd,
            "ml_prediction_direction": prediction_direction,
            "reasons": reasons,
            "execution_enabled": False
        }
