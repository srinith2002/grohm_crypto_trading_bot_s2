class AIExplanationAgent:

    def explain(self, workflow_data):

        decision = workflow_data.get("decision", {})
        technical = workflow_data.get("technical_analysis", {})
        strategy = workflow_data.get("strategy_analysis", {})
        risk = workflow_data.get("risk_analysis", {})
        ml = workflow_data.get("ml_prediction", {})

        final_decision = decision.get("decision", "UNKNOWN")
        trend = decision.get("technical_trend", "UNKNOWN")
        macd = decision.get("macd_condition", "UNKNOWN")
        signal = strategy.get("signal", "UNKNOWN")
        risk_status = risk.get("risk_status", "UNKNOWN")

        reasons = []

        reasons.append(
            f"The technical trend is {trend}."
        )

        reasons.append(
            f"The MACD condition is {macd}."
        )

        reasons.append(
            f"The strategy generated a {signal} signal "
            f"with a score of {strategy.get('total_score')}."
        )

        reasons.append(
            f"Risk analysis returned {risk_status}: "
            f"{risk.get('reason', 'No additional details')}."
        )

        reasons.append(
            f"The ensemble prediction was "
            f"{ml.get('ensemble_prediction')} compared "
            f"with the recorded actual close of "
            f"{ml.get('actual_close')}."
        )

        if final_decision == "HOLD":
            summary = (
                "GROHM recommends HOLD because the strategy "
                "did not generate a candidate signal and "
                "risk checks were not approved."
            )
        else:
            summary = (
                f"The workflow produced {final_decision}. "
                "Further paper-trading review is required."
            )

        return {
            "agent": "AI Explanation Agent",
            "status": "SUCCESS",
            "final_decision": final_decision,
            "summary": summary,
            "explanation": reasons,
            "execution_enabled": False
        }