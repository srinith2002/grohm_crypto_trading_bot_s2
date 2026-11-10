
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# GROHM AI STRATEGY OPTIMIZER
# Historical paper simulation only
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "candles"

INPUT_FILE = DATA_DIR / "BTCUSD_30m_risk_results.csv"

SUMMARY_FILE = DATA_DIR / "BTCUSD_30m_strategy_optimizer.csv"
TRADES_FILE = DATA_DIR / "BTCUSD_30m_strategy_optimizer_trades.csv"

STRATEGIES = {
    "Conservative": 80,
    "Moderate": 70,
    "Exploratory": 60
}

MAX_HOLDING_CANDLES = 48


def calculate_max_drawdown(pnl_values):
    if not pnl_values:
        return 0.0

    equity = pd.Series(pnl_values).cumsum()
    peak = equity.cummax()
    drawdown = peak - equity

    return round(float(drawdown.max()), 2)


def simulate_strategy(df, strategy_name, threshold):

    candidates = df[
        (df["signal"] == "LONG_CANDIDATE") &
        (df["status"] == "APPROVED") &
        (df["total_score"] >= threshold)
    ]

    trade_records = []
    pnl_values = []

    busy_until = -1
    simulated_count = 0
    ambiguous_count = 0
    unresolved_count = 0
    wins = 0
    losses = 0

    for i in candidates.index:

        # Avoid overlapping simulated trades.
        if i <= busy_until:
            continue

        entry = df.iloc[i]

        entry_price = entry["close"]
        stop_loss = entry["stop_loss"]
        take_profit = entry["take_profit"]
        position_size = entry["position_size"]

        if pd.isna(entry_price) or pd.isna(stop_loss) or pd.isna(take_profit):
            continue

        future = df.iloc[i + 1:i + 1 + MAX_HOLDING_CANDLES]

        if future.empty:
            unresolved_count += 1
            busy_until = len(df) - 1
            continue

        outcome = None
        exit_price = None
        exit_time = None
        exit_index = None

        for j, candle in zip(future.index, future.itertuples()):

            stop_hit = candle.low <= stop_loss
            target_hit = candle.high >= take_profit

            # Both levels touched in the same candle:
            # candle data cannot establish which happened first.
            if stop_hit and target_hit:
                outcome = "AMBIGUOUS"
                exit_time = candle.time
                exit_index = j
                break

            if stop_hit:
                outcome = "LOSS"
                exit_price = stop_loss
                exit_time = candle.time
                exit_index = j
                break

            if target_hit:
                outcome = "WIN"
                exit_price = take_profit
                exit_time = candle.time
                exit_index = j
                break

        if outcome == "AMBIGUOUS":
            ambiguous_count += 1
            busy_until = exit_index

            trade_records.append({
                "strategy": strategy_name,
                "threshold": threshold,
                "entry_time": entry["time"],
                "entry_price": entry_price,
                "outcome": "AMBIGUOUS",
                "simulated_pnl": None
            })
            continue

        if outcome is None:
            last_candle = future.iloc[-1]
            outcome = "TIME_EXIT"
            exit_price = last_candle["close"]
            exit_time = last_candle["time"]
            exit_index = future.index[-1]

        # Long-only simulated P&L.
        simulated_pnl = (
            position_size * (exit_price - entry_price)
        )

        simulated_pnl = round(float(simulated_pnl), 2)

        if outcome == "WIN":
            wins += 1
        elif outcome == "LOSS":
            losses += 1

        pnl_values.append(simulated_pnl)
        simulated_count += 1
        busy_until = exit_index

        trade_records.append({
            "strategy": strategy_name,
            "threshold": threshold,
            "entry_time": entry["time"],
            "exit_time": exit_time,
            "entry_price": entry_price,
            "exit_price": exit_price,
            "outcome": outcome,
            "simulated_pnl": simulated_pnl
        })

    completed = wins + losses

    win_rate = (
        wins / completed * 100
        if completed > 0 else 0
    )

    summary = {
        "strategy": strategy_name,
        "score_threshold": threshold,
        "eligible_setups": len(candidates),
        "simulated_trades": simulated_count,
        "wins": wins,
        "losses": losses,
        "ambiguous": ambiguous_count,
        "unresolved": unresolved_count,
        "win_rate_percent": round(win_rate, 2),
        "simulated_pnl": round(sum(pnl_values), 2),
        "max_drawdown": calculate_max_drawdown(pnl_values)
    }

    return summary, trade_records


def main():

    if not INPUT_FILE.exists():
        print("Risk results file not found:", INPUT_FILE)
        return

    df = pd.read_csv(INPUT_FILE)

    required_columns = [
        "time", "open", "high", "low", "close",
        "signal", "status", "total_score",
        "stop_loss", "take_profit", "position_size"
    ]

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing:
        print("Missing columns:", missing)
        return

    df["time"] = pd.to_datetime(df["time"], errors="coerce")

    numeric_columns = [
        "open", "high", "low", "close",
        "total_score", "stop_loss",
        "take_profit", "position_size"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = (
        df.dropna(subset=required_columns)
        .sort_values("time")
        .reset_index(drop=True)
    )

    all_summaries = []
    all_trades = []

    for strategy_name, threshold in STRATEGIES.items():

        summary, trades = simulate_strategy(
            df,
            strategy_name,
            threshold
        )

        all_summaries.append(summary)
        all_trades.extend(trades)

        print("\n", strategy_name)
        print(summary)

    pd.DataFrame(all_summaries).to_csv(
        SUMMARY_FILE, index=False
    )

    pd.DataFrame(all_trades).to_csv(
        TRADES_FILE, index=False
    )

    print("\nStrategy comparison saved:", SUMMARY_FILE)
    print("Trade details saved:", TRADES_FILE)


if __name__ == "__main__":
    main()
