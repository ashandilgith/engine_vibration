# --- train_model.py (Regression Version) ---
import pandas as pd
import numpy as np
import os
import xgboost as xgb
from sklearn.model_selection import train_test_split

def main():
    """Trains an XGBoost model to predict normal vibration."""
    print("--- Starting Regression Model Training ---")
    
    data_path = os.path.join('data', 'raw_data.csv')
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Please run generate_data.py")
        return

    df = pd.read_csv(data_path)
    df.dropna(inplace=True)

    # --- Feature & Target Definition ---
    # The model will learn to predict the 'actual' vibration based on the conditions
    features = ['rpm', 'ambient_temp_c', 'fuel_level_percent', 'sea_state']
    target = 'az_vibration_actual'

    X = df[features]
    y = df[target]

    # --- Model Training ---
    # We will train on the 'healthy' portion of the data (first 60%)
    # This teaches the model what "normal" looks like before the fault gets bad
    healthy_cutoff = int(len(df) * 0.6)
    X_train = X.iloc[:healthy_cutoff]
    y_train = y.iloc[:healthy_cutoff]

    # Initialize and train the XGBoost Regressor
    model = xgb.XGBRegressor(
        objective='reg:squarederror',
        n_estimators=1000,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1 # Use all available CPU cores
    )
    
    print("\nStarting model training...")
    model.fit(X_train, y_train, verbose=False)
    
    # --- Save Model and Calculate Anomaly Threshold ---
    model_dir = 'models'
    os.makedirs(model_dir, exist_ok=True)
    model.save_model(os.path.join(model_dir, 'vibration_regressor.json'))
    print(f"\nModel saved to: {model_dir}/vibration_regressor.json")

    # The key step: Use the trained model to predict what the vibration *should* have been
    # for the healthy data, then find the error.
    y_pred_healthy = model.predict(X_train)
    errors = np.abs(y_train - y_pred_healthy)
    
    # The anomaly threshold is a level of error that is unusual for a healthy machine
    anomaly_threshold = np.percentile(errors, 99) * 1.5 # 99th percentile, with a buffer
    
    np.save(os.path.join(model_dir, 'regression_anomaly_threshold.npy'), anomaly_threshold)
    print(f"Anomaly threshold ({anomaly_threshold:.4f}) saved to: {model_dir}/regression_anomaly_threshold.npy")

if __name__ == "__main__":
    main()
