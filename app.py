# --- app.py (Regression Version) ---
import gradio as gr
import numpy as np
import pandas as pd
import os
import xgboost as xgb

# --- Load Model and Threshold ---
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'models', 'vibration_regressor.json')
threshold_path = os.path.join(base_dir, 'models', 'regression_anomaly_threshold.npy')

try:
    model = xgb.XGBRegressor()
    model.load_model(model_path)
    anomaly_threshold = np.load(threshold_path)
    print("Model and threshold loaded successfully.")
except Exception as e:
    print(f"CRITICAL ERROR: Could not load files. Details: {e}")
    model = None
    anomaly_threshold = None

description = """
<div align="center">
  <img src="https://images.pexels.com/photos/6510296/pexels-photo-6510296.jpeg" width="600px" />
</div>
**Zodiac 1.0: Regression-Based Engine Diagnostics.**
This advanced model predicts the **normal** vibration for your engine based on its current operating conditions. Enter the conditions and the actual vibration reading from your sensor to check for anomalies.
"""

def predict_anomaly(rpm, temp, fuel, sea_state, actual_vibration):
    """Predicts if the actual vibration is an anomaly given the conditions."""
    if model is None:
        return "Error: Model not loaded.", "", ""

    try:
        # Map sea state string to integer
        sea_state_map = {"Calm": 0, "Choppy": 1, "Stormy": 2}
        sea_state_int = sea_state_map.get(sea_state, 0)
        
        # Create a DataFrame with the exact feature names the model was trained on
        input_data = pd.DataFrame([{
            'rpm': rpm,
            'ambient_temp_c': temp,
            'fuel_level_percent': fuel,
            'sea_state': sea_state_int
        }])
        
        # Predict the expected normal vibration
        predicted_vibration = model.predict(input_data)[0]
        
        # Calculate the error
        error = abs(actual_vibration - predicted_vibration)
        
        status = "🚨 ANOMALY DETECTED 🚨" if error > anomaly_threshold else "✅ Machine State: Normal"
        
        details = f"Predicted Normal Vibration: {predicted_vibration:.2f}\n"
        details += f"Actual Measured Vibration: {actual_vibration:.2f}\n"
        details += f"Calculated Error: {error:.4f}\n"
        details += f"Anomaly Threshold: {anomaly_threshold:.4f}"
        
        return status, details
    except Exception as e:
        return f"An error occurred: {e}", ""

# --- Create the Gradio Interface with sliders and dropdowns for conditions ---
demo = gr.Interface(
    fn=predict_anomaly,
    inputs=[
        gr.Slider(800, 5000, value=2500, label="Engine RPM"),
        gr.Slider(25, 40, value=32, label="Ambient Temperature (°C)"),
        gr.Slider(0, 100, value=75, label="Fuel Level (%)"),
        gr.Dropdown(["Calm", "Choppy", "Stormy"], value="Calm", label="Current Sea State"),
        gr.Number(label="Actual Measured Vibration (from your sensor)")
    ],
    outputs=[
        gr.Textbox(label="Prediction Status"),
        gr.Textbox(label="Analysis Details")
    ],
    title="PiranaWare Boat Engine Predictive Maintenance",
    description=description,
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    if model is not None:
        demo.launch()
    else:
        print("Gradio app will not launch because the model could not be loaded.")
