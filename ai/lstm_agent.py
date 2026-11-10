
import pandas as pd
import numpy as np
import joblib

from pathlib import Path
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping


# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = BASE_DIR / "data/candles/BTCUSD_30m_indicators.csv"

MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_FILE = MODEL_DIR / "lstm_model.keras"
SCALER_FILE = MODEL_DIR / "lstm_scaler.pkl"

RESULT_FILE = BASE_DIR / "data/candles/BTCUSD_30m_lstm_results.csv"
PREDICTION_FILE = BASE_DIR / "data/candles/BTCUSD_30m_lstm_prediction.csv"

SEQUENCE_LENGTH = 30


def run_lstm():

    # 1. Load historical data
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE)

    if "close" in df.columns:
        close_column = "close"
    elif "Close" in df.columns:
        close_column = "Close"
    else:
        raise ValueError("Close column not found in input file.")

    df[close_column] = pd.to_numeric(
        df[close_column], errors="coerce"
    )

    df = df.dropna(subset=[close_column]).reset_index(drop=True)

    prices = df[close_column].to_numpy(dtype=float)

    if len(prices) < 100:
        raise ValueError("At least 100 valid closing prices are required.")

    if not np.isfinite(prices).all():
        raise ValueError("Closing prices contain invalid values.")

    if np.any(prices <= 0):
        raise ValueError("Closing prices must be positive.")

    print("Total candles:", len(prices))

    # 2. Chronological 80:20 split
    split_index = int(len(prices) * 0.80)

    train_prices = prices[:split_index]

    # 3. Fit scaler only on training data
    scaler = MinMaxScaler(feature_range=(0, 1))

    scaler.fit(train_prices.reshape(-1, 1))

    scaled_prices = scaler.transform(
        prices.reshape(-1, 1)
    )

    joblib.dump(scaler, SCALER_FILE)

    # 4. Create 30-candle sequences
    X_train = []
    y_train = []

    X_test = []
    y_test = []
    test_actual_indices = []

    for i in range(SEQUENCE_LENGTH, len(prices)):

        sequence = scaled_prices[i-SEQUENCE_LENGTH:i]
        target = scaled_prices[i]

        if i < split_index:
            X_train.append(sequence)
            y_train.append(target)
        else:
            X_test.append(sequence)
            y_test.append(target)
            test_actual_indices.append(i)

    X_train = np.array(X_train)
    y_train = np.array(y_train)

    X_test = np.array(X_test)
    y_test = np.array(y_test)

    print("Training samples:", len(X_train))
    print("Testing samples:", len(X_test))

    # 5. Build LSTM model
    model = Sequential([
        LSTM(
            50,
            activation="tanh",
            input_shape=(SEQUENCE_LENGTH, 1)
        ),
        Dense(1)
    ])

    model.compile(
        optimizer="adam",
        loss="mean_squared_error"
    )

    # 6. Train model
    early_stop = EarlyStopping(
        monitor="val_loss",
        patience=3,
        restore_best_weights=True
    )

    model.fit(
        X_train,
        y_train,
        epochs=20,
        batch_size=16,
        validation_split=0.1,
        shuffle=False,
        callbacks=[early_stop],
        verbose=1
    )

    # Save trained model
    model.save(MODEL_FILE)

    # 7. Test model
    scaled_predictions = model.predict(
        X_test, verbose=0
    )

    actual_prices = scaler.inverse_transform(
        y_test.reshape(-1, 1)
    ).flatten()

    predicted_prices = scaler.inverse_transform(
        scaled_predictions
    ).flatten()

    # 8. Calculate MAE and RMSE
    mae = mean_absolute_error(
        actual_prices, predicted_prices
    )

    rmse = np.sqrt(
        mean_squared_error(actual_prices, predicted_prices)
    )

    results = pd.DataFrame({
        "Actual_Close": actual_prices,
        "Predicted_Close": predicted_prices,
        "Absolute_Error": np.abs(
            actual_prices - predicted_prices
        )
    })

    results.to_csv(RESULT_FILE, index=False)

    # 9. Estimate next candle closing price
    last_30_candles = scaled_prices[-SEQUENCE_LENGTH:]

    next_input = last_30_candles.reshape(
        1, SEQUENCE_LENGTH, 1
    )

    next_scaled_prediction = model.predict(
        next_input, verbose=0
    )

    next_price = scaler.inverse_transform(
        next_scaled_prediction
    )[0][0]

    prediction_result = pd.DataFrame([{
        "Current_Close": prices[-1],
        "LSTM_Predicted_Next_Close": next_price
    }])

    prediction_result.to_csv(
        PREDICTION_FILE, index=False
    )

    # 10. Display results
    print("\nGROHM LSTM RESULTS")

    print("MAE:", round(mae, 4))
    print("RMSE:", round(rmse, 4))

    print("\nNext Candle Price Estimate:")
    print(round(next_price, 4))

    print("\nSaved files:")
    print(MODEL_FILE)
    print(SCALER_FILE)
    print(RESULT_FILE)
    print(PREDICTION_FILE)


if __name__ == "__main__":
    run_lstm()
