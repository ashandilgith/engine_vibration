# --- data_logger.py ---
from flask import Flask, request
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

# Define the data directory and the full path for the CSV file
DATA_DIR = 'data'
CSV_FILE = os.path.join(DATA_DIR, 'raw_data.csv')

@app.route('/data', methods=['POST'])
def receive_data():
    try:
        # Ensure the data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)
        
        data = request.get_json()
        log_data = {
            'timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            'ax': [data.get('ax')], 'ay': [data.get('ay')], 'az': [data.get('az')],
            'gx': [data.get('gx')], 'gy': [data.get('gy')], 'gz': [data.get('gz')],
            'temperature_c': [data.get('temperature_c')]
        }
        df_new = pd.DataFrame(log_data)
        
        if not os.path.exists(CSV_FILE):
            df_new.to_csv(CSV_FILE, index=False, header=True)
        else:
            df_new.to_csv(CSV_FILE, mode='a', index=False, header=False)
        return "Data received successfully", 200
    except Exception as e:
        return "Error", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
