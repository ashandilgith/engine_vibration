# --- app.py ---
import gradio as gr, numpy as np, pandas as pd, io, os
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

try:
    model = load_model('models/time_series_model.h5')
    anomaly_threshold = np.load('models/anomaly_threshold.npy')
except Exception as e:
    model = None; anomaly_threshold = 999
WINDOW_SIZE = 50

def predict_anomaly(data_string):
    if model is None: return "Error: Model not loaded.", ""
    try:
        df = pd.read_csv(io.StringIO(data_string), header=None, names=['ax','ay','az','gx','gy','gz','temperature_c'])
        if len(df) < WINDOW_SIZE + 1: return f"Not enough data. Need at least {WINDOW_SIZE + 1} rows.", ""
        az_data = df[['az']].values
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(az_data)
        def create_windows(data, window_size):
            X, y = [], []
            for i in range(len(data) - window_size):
                X.append(data[i:(i + window_size)]); y.append(data[i + window_size])
            return np.array(X), np.array(y)
        X_new, y_new = create_windows(scaled_data, WINDOW_SIZE)
        if len(X_new) == 0: return "Not enough data to form a full window.", ""
        predictions = model.predict(X_new)
        mae_loss = np.mean(np.abs(predictions - y_new), axis=1)
        last_loss = mae_loss[-1]
        status = "🚨 ANOMALY DETECTED 🚨" if last_loss > anomaly_threshold else "✅ Machine State: Normal"
        details = f"Calculated Error: {last_loss:.4f}\nAnomaly Threshold: {anomaly_threshold:.4f}"
        return status, details
    except Exception as e:
        return f"An error occurred: {e}", ""

demo = gr.Interface(fn=predict_anomaly, inputs=gr.Textbox(lines=10, label=f"Paste Sensor Data (CSV format, at least {WINDOW_SIZE+1} rows)"), outputs=[gr.Textbox(label="Prediction Status"), gr.Textbox(label="Details")], title="Predictive Maintenance Anomaly Detector")
if __name__ == "__main__":
    demo.launch()
