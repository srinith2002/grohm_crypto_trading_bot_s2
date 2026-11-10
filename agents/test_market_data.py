from market_data_agent import fetch_market_data

if __name__ == "__main__":

    df = fetch_market_data(
        symbol="BTCUSD",
        resolution="30m",
        limit=300
    )

    print("\nLatest Market Candles:")
    print(df.tail())

    print("\nData Shape:")
    print(df.shape)


