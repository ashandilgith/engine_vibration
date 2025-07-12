# --- train_model.py ---
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def create_windows(data, window_size):
    """Helper function to create windowed data for time-series forecasting."""
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:(i + window_size)])
        y.append(data[i + window_size])
    return np.array(X), np.array(y)

def main():
    """Main function to run the EDA, preprocessing, and training pipeline."""
    # --- 1. Load and Explore Data ---
    print("--- Starting EDA and Cleaning ---")
    
    data_path = os.path.join('data', 'raw_data.csv')

    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Please generate it first by running generate_practice_data.py")
        return

    df = pd.read_csv(data_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    print("Data Info:")
    df.info()

    # Save EDA plot to a file instead of showing it interactively
    print("\nPlotting raw sensor data...")
    df.plot(subplots=True, figsize=(15, 12), title="Sensor Data Over Time")
    plt.savefig('eda_raw_plots.png')
    plt.close() # Close the plot to prevent it from displaying in some environments
    print("Saved raw data plots to eda_raw_plots.png")

    # --- 2. Preprocessing ---
    df.fillna(method='ffill', inplace=True)
    df_smooth = df.rolling(window=5).mean().dropna()
    print("\nData cleaned and smoothed.")

    # --- 3. Model Training ---
    print("\n--- Training Time-Series Anomaly Detection Model ---")
    
    healthy_cutoff = int(len(df_smooth) * 0.6)
    df_healthy = df_smooth.iloc[:healthy_cutoff]

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df_healthy[['az']])

    WINDOW_SIZE = 50
    X_train, y_train = create_windows(scaled_data, WINDOW_SIZE)

    # Build the LSTM model
    model = Sequential([
        LSTM(64, input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences=True),
        Dropout(0.2),
        LSTM(32, return_sequences=False),
        Dropout(0.2),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    print("\nModel Summary:")
    model.summary()

    print("\nStarting model training...")
    model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.1, verbose=1)
    
    # --- 4. Save Model and Threshold ---
    os.makedirs('models', exist_ok=True)
    # FIX: Save in the recommended .keras format
    model.save('models/time_series_model.keras') 

    # Calculate anomaly threshold on the same healthy data
    train_pred = model.predict(X_train)
    train_mae_loss = np.mean(np.abs(train_pred - y_train), axis=1)
    anomaly_threshold = np.max(train_mae_loss) * 1.5 
    np.save('models/anomaly_threshold.npy', anomaly_threshold)
    
    print(f"\nTraining complete.")
    print(f"Model saved to: models/time_series_model.keras")
    print(f"Anomaly threshold ({anomaly_threshold:.4f}) saved to: models/anomaly_threshold.npy")

if __name__ == "__main__":
    main()
