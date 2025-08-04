# --- data_logger.py (Regression Version) ---
import pandas as pd
import os
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)

DATA_DIR = 'data'
CSV_FILE = os.path.join(DATA_DIR, 'raw_data.csv')

@app.route('/data', methods=['POST'])
def receive_data():
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        data = request.get_json()
        
        # Define the columns to match the new hardware output and training script
        log_data = {
            'rpm': [data.get('rpm')],
            'ambient_temp_c': [data.get('ambient_temp_c')],
            'fuel_level_percent': [data.get('fuel_level_percent')],
            'sea_state': [data.get('sea_state')],
            'az_vibration_actual': [data.get('az_vibration_actual')]
        }
        
        df_new = pd.DataFrame(log_data)
        
        if not os.path.exists(CSV_FILE):
            df_new.to_csv(CSV_FILE, index=False, header=True)
        else:
            df_new.to_csv(CSV_FILE, mode='a', index=False, header=False)
            
        print(f"Logged: {log_data}")
        return "Data received successfully", 200
    except Exception as e:
        print(f"Error: {e}")
        return "Error", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
