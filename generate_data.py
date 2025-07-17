# --- generate_data.py (Regression Version) ---
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_data(filename="raw_data.csv", total_rows=10000):
    """
    Generates a dataset where vibration is a function of multiple operating conditions.
    """
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)
    filepath = os.path.join(data_dir, filename)

    print(f"Generating regression dataset with {total_rows} rows...")
    
    # Simulate different conditions
    rpms = np.random.randint(800, 4500, total_rows)
    ambient_temps = np.random.uniform(28, 35, total_rows) # Tropical temps
    fuel_levels = np.random.uniform(10, 100, total_rows) # Percentage
    # 0=Calm, 1=Choppy, 2=Stormy
    sea_states = np.random.choice([0, 1, 2], total_rows, p=[0.6, 0.3, 0.1])

    # --- The Core Logic: Vibration is a function of conditions ---
    # Base vibration increases with the square of RPM
    base_vibration = 9.8 + (rpms / 1000)**2 
    
    # Temperature adds a small linear effect
    temp_effect = (ambient_temps - 28) * 0.05
    
    # Sea state adds random noise
    sea_effect = np.random.normal(0, sea_states * 0.2)
    
    # A developing fault adds a slow, growing trend over time
    fault_trend = np.linspace(0, 1, total_rows) * 3.0
    
    # Combine all effects to get the final measured vibration
    az_vibration = base_vibration + temp_effect + sea_effect + fault_trend

    df = pd.DataFrame({
        'rpm': rpms,
        'ambient_temp_c': ambient_temps,
        'fuel_level_percent': fuel_levels,
        'sea_state': sea_states,
        'az_vibration_actual': az_vibration
    })
    
    df.to_csv(filepath, index=False)
    print(f"Successfully generated and saved data to '{filepath}'")

if __name__ == "__main__":
    generate_data()
