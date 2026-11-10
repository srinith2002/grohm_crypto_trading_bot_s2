
from performance_analysis_agent import analyze_performance


if __name__ == "__main__":

    input_file = (
        "data/candles/BTCUSD_30m_trade_monitoring.csv"
    )

    output_file = (
        "data/candles/BTCUSD_30m_performance.csv"
    )

    analyze_performance(input_file, output_file)
