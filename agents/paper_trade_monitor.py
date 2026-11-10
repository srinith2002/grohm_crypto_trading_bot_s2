
import pandas as pd


def monitor_paper_trades(trades_file, candles_file, output_file):

    print("Loading paper trades...")
    trades = pd.read_csv(trades_file)

    print("Loading market candles...")
    candles = pd.read_csv(candles_file)

    trades["entry_time"] = pd.to_datetime(
        trades["entry_time"], utc=True
    )

    candles["time"] = pd.to_datetime(
        candles["time"], utc=True
    )

    candles = candles.sort_values("time")

    results = []

    print("Monitoring simulated trades...")

    for _, trade in trades.iterrows():

        entry_time = trade["entry_time"]
        entry_price = float(trade["entry_price"])
        stop_loss = float(trade["stop_loss"])
        take_profit = float(trade["take_profit"])
        quantity = float(trade["position_size"])
        signal = trade["signal"]

        future_candles = candles[
            candles["time"] > entry_time
        ]

        status = "OPEN"
        exit_time = None
        exit_price = None
        pnl = None

        for _, candle in future_candles.iterrows():

            high = float(candle["high"])
            low = float(candle["low"])

            if signal == "LONG_CANDIDATE":
                sl_hit = low <= stop_loss
                tp_hit = high >= take_profit

            elif signal == "SHORT_CANDIDATE":
                sl_hit = high >= stop_loss
                tp_hit = low <= take_profit

            else:
                continue

            if sl_hit and tp_hit:
                status = "AMBIGUOUS"
                exit_time = candle["time"]
                break

            elif sl_hit:
                status = "LOSS"
                exit_time = candle["time"]
                exit_price = stop_loss
                break

            elif tp_hit:
                status = "WIN"
                exit_time = candle["time"]
                exit_price = take_profit
                break

        if exit_price is not None:

            if signal == "LONG_CANDIDATE":
                pnl = (exit_price - entry_price) * quantity
            else:
                pnl = (entry_price - exit_price) * quantity

        results.append({
            "entry_time": entry_time,
            "signal": signal,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "position_size": quantity,
            "exit_time": exit_time,
            "exit_price": exit_price,
            "trade_status": status,
            "simulated_pnl": (
                round(pnl, 2) if pnl is not None else None
            )
        })

    results_df = pd.DataFrame(results)

    results_df.to_csv(output_file, index=False)

    print("\nPaper Trade Monitoring Completed!")

    print(results_df.tail(10))

    print("\nTrade Status Summary:")
    print(results_df["trade_status"].value_counts())

    print("\nSaved successfully:", output_file)

