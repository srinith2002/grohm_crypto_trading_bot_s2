import pandas as pd
def analyze_performance(input_file, output_file):
    print("Loading trade monitoring data...")

    df = pd.read_csv(input_file)

    completed = df[
        df["trade_status"].isin(["WIN", "LOSS"])
    ].copy()

    total_trades = len(completed)

    wins = (completed["trade_status"] == "WIN").sum()
    losses = (completed["trade_status"] == "LOSS").sum()

    win_rate = (
        wins / total_trades * 100
        if total_trades > 0 else 0
    )

    pnl = pd.to_numeric(
        completed["simulated_pnl"],
        errors="coerce"
    ).fillna(0)

    total_pnl = pnl.sum()

    report = pd.DataFrame([{
        "total_trades": total_trades,
        "winning_trades": wins,
        "losing_trades": losses,
        "win_rate": round(win_rate, 2),
        "total_simulated_pnl": round(total_pnl, 2)
    }])

    report.to_csv(output_file, index=False)

    print("\nPerformance Analysis Results:")
    print(report)

    print("\nSaved successfully:", output_file)

