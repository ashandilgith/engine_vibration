# --- app.py ---
import gradio as gr, numpy as np, pandas as pd, io, os
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

# Build absolute paths to the model files to ensure they are found
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'models', 'time_series_model.keras')
threshold_path = os.path.join(base_dir, 'models', 'anomaly_threshold.npy')

# Load model and threshold with error checking
try:
    if not os.path.exists(model_path) or not os.path.exists(threshold_path):
        raise FileNotFoundError("Model or threshold file not found. Please run 'train_model.py' first.")
    model = load_model(model_path)
    anomaly_threshold = np.load(threshold_path)
    print("Model and threshold loaded successfully.")
except Exception as e:
    print(f"CRITICAL ERROR: Could not load model files.")
    print(f"Details: {e}")
    model = None
    anomaly_threshold = None

WINDOW_SIZE = 50

# --- NEW: Define the description with Markdown for aesthetics ---
description = """
<div align="center">
  <img src="https://images.pexels.com/photos/15737317/pexels-photo-15737317.jpeg" />
</div>

**Zodiac 1.0: Your Engine's Early-Warning System.**

This MVP uses a trained AI model to analyze engine vibration data. It predicts potential mechanical failures by detecting subtle anomalies that are invisible to the human eye. 
Paste your sensor data below to see a real-time health check.
"""

def predict_anomaly(data_string):
    if model is None:
        return "Error: Model not loaded. Please check the terminal for details.", ""

    try:
        df = pd.read_csv(io.StringIO(data_string), header=None, names=['ax','ay','az','gx','gy','gz','temperature_c'])
        if len(df) < WINDOW_SIZE + 1:
            return f"Not enough data. Please provide at least {WINDOW_SIZE + 1} rows.", ""
        
        az_data = df[['az']].values
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(az_data)

        def create_windows(data, window_size):
            X, y = [], []
            for i in range(len(data) - window_size):
                X.append(data[i:(i + window_size)])
                y.append(data[i + window_size])
            return np.array(X), np.array(y)

        X_new, y_new = create_windows(scaled_data, WINDOW_SIZE)
        if len(X_new) == 0:
            return "Not enough data to form a full window.", ""

        predictions = model.predict(X_new)
        mae_loss = np.mean(np.abs(predictions - y_new), axis=1)
        last_loss = mae_loss[-1]
        
        status = "🚨 ANOMALY DETECTED 🚨" if last_loss > anomaly_threshold else "✅ Machine State: Normal"
        details = f"Calculated Error: {last_loss:.4f}\nAnomaly Threshold: {anomaly_threshold:.4f}"
        return status, details
    except Exception as e:
        return f"An error occurred during prediction: {e}", ""

# --- NEW: Update the Interface with the new title and description ---
demo = gr.Interface(
    fn=predict_anomaly,
    inputs=gr.Textbox(lines=10, label=f"Paste Sensor Data (CSV format, at least {WINDOW_SIZE+1} rows)"),
    outputs=[gr.Textbox(label="Prediction Status"), gr.Textbox(label="Details")],
    title="Zodiac 1.0 Boat Engine Monitoring",
    description=description,
    theme=gr.themes.Soft() # Added a theme for better aesthetics
)

if __name__ == "__main__":
    if model is not None:
        demo.launch()
    else:
        print("Gradio app will not launch because the model could not be loaded.")
