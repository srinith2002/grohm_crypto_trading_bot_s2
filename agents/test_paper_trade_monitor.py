from paper_trade_monitor import monitor_paper_trades


if __name__ == "__main__":

    trades_file = (
        "data/candles/BTCUSD_30m_paper_trades.csv"
    )

    candles_file = (
        "data/candles/BTCUSD_30m_indicators.csv"
    )

    output_file = (
        "data/candles/BTCUSD_30m_trade_monitoring.csv"
    )

    monitor_paper_trades(
        trades_file,
        candles_file,
        output_file
    )
