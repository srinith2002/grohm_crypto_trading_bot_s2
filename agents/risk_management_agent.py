import pandas as pd


def evaluate_risk(
    row,
    paper_capital=10000,
    risk_budget=50,
    max_capital_fraction=0.20,
    reward_risk_ratio=2.0,
    atr_multiplier=1.5
):

    signal = row["signal"]
    entry_price = float(row["close"])
    atr = float(row["ATR_14"])

    result = {
        "status": "REJECTED",
        "reason": "",
        "stop_loss": None,
        "take_profit": None,
        "position_size": 0,
        "risk_amount": 0,
        "potential_reward": 0
    }

    if signal not in ["LONG_CANDIDATE", "SHORT_CANDIDATE"]:
        result["reason"] = "No candidate signal"
        return result

    if pd.isna(entry_price) or pd.isna(atr):
        result["reason"] = "Missing price or ATR"
        return result

    if entry_price <= 0 or atr <= 0:
        result["reason"] = "Invalid price or ATR"
        return result

    stop_distance = atr * atr_multiplier

    if signal == "LONG_CANDIDATE":
        stop_loss = entry_price - stop_distance
        take_profit = entry_price + (
            stop_distance * reward_risk_ratio
        )
    else:
        stop_loss = entry_price + stop_distance
        take_profit = entry_price - (
            stop_distance * reward_risk_ratio
        )

    risk_per_unit = stop_distance

    risk_based_size = risk_budget / risk_per_unit

    max_allocation = paper_capital * max_capital_fraction

    capital_based_size = max_allocation / entry_price

    position_size = min(
        risk_based_size,
        capital_based_size
    )

    actual_risk = position_size * risk_per_unit

    potential_reward = (
        position_size * stop_distance * reward_risk_ratio
    )

    result.update({
        "status": "APPROVED",
        "reason": "Passed paper risk checks",
        "stop_loss": round(stop_loss, 2),
        "take_profit": round(take_profit, 2),
        "position_size": round(position_size, 6),
        "risk_amount": round(actual_risk, 2),
        "potential_reward": round(potential_reward, 2)
    })

    return result