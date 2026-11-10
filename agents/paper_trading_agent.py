
import pandas as pd


def create_paper_trades(input_file, output_file):

    print("Loading risk management results...")

    df = pd.read_csv(input_file)

    print("Filtering approved signals...")

    approved = df[df["status"] == "APPROVED"].copy()

    if approved.empty:
        print("No approved signals found.")
        return

    required_columns = [
        "time",
        "signal",
        "close",
        "stop_loss",
        "take_profit",
        "position_size",
        "risk_amount",
        "potential_reward"
    ]

    missing = [
        col for col in required_columns
        if col not in approved.columns
    ]

    if missing:
        print("Missing columns:", missing)
        return

    trades = approved[required_columns].copy()

    trades.rename(columns={
        "time": "entry_time",
        "close": "entry_price"
    }, inplace=True)

    trades["trade_status"] = "OPEN_SIMULATION"

    trades.to_csv(output_file, index=False)

    print("\nPaper trades created successfully!")

    print(trades.tail())

    print("\nSaved successfully:", output_file)

