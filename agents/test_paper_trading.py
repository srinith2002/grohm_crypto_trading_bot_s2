
from paper_trading_agent import create_paper_trades


if __name__ == "__main__":

    input_file = "data/candles/BTCUSD_30m_risk_results.csv"

    output_file = "data/candles/BTCUSD_30m_paper_trades.csv"

    create_paper_trades(input_file, output_file)
