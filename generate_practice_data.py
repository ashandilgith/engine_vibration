# --- generate_practice_data.py ---
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_data(filename="raw_data.csv", total_rows=5000):
    print(f"Generating synthetic dataset with {total_rows} rows...")
    start_time = datetime.now() - timedelta(hours=10)
    timestamps = [start_time + timedelta(seconds=i*2) for i in range(total_rows)]
    ax = np.random.normal(0.0, 0.05, total_rows)
    ay = np.random.normal(0.0, 0.05, total_rows)
    az = np.random.normal(9.8, 0.1, total_rows)
    gx = np.random.normal(0.0, 0.1, total_rows)
    gy = np.random.normal(0.0, 0.1, total_rows)
    gz = np.random.normal(0.0, 0.1, total_rows)
    temp = np.random.normal(45.0, 0.5, total_rows)
    fault_start_index = int(total_rows * 0.6)
    fault_duration = total_rows - fault_start_index
    fault_trend = np.linspace(0, 1, fault_duration)
    az[fault_start_index:] += fault_trend * 2.5
    az[fault_start_index:] += np.random.normal(0, 0.2 * fault_trend, fault_duration)
    temp[fault_start_index:] += fault_trend * 30
    df = pd.DataFrame({'timestamp': timestamps, 'ax': ax, 'ay': ay, 'az': az, 'gx': gx, 'gy': gy, 'gz': gz, 'temperature_c': temp})
    df.to_csv(filename, index=False)
    print(f"Successfully generated and saved data to '{filename}'")

if __name__ == "__main__":
    generate_data()
