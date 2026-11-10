import pandas as pd
from risk_management_agent import evaluate_risk


if __name__ == "__main__":

    file_path = "data/candles/BTCUSD_30m_flexi_matrix.csv"

    print("Loading Flexi Matrix data...")

    df = pd.read_csv(file_path)

    print("Running Risk Management Agent...")

    results = df.apply(evaluate_risk, axis=1)

    results_df = pd.DataFrame(results.tolist())

    final_df = pd.concat(
        [df.reset_index(drop=True),
         results_df.reset_index(drop=True)],
        axis=1
    )

    print("\nRisk Management Results:")

    print(final_df[[
        "close",
        "signal",
        "status",
        "stop_loss",
        "take_profit",
        "position_size",
        "risk_amount",
        "potential_reward"
    ]].tail(10))

    output_file = "data/candles/BTCUSD_30m_risk_results.csv"

    final_df.to_csv(output_file, index=False)

    print("\nSaved successfully:", output_file)