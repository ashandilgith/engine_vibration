title: Zodiac 1.0 Engine Monitor
emoji: 🛥️
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.29.0
app_file: app.py
pinned: false
---

# Zodiac 1.0: Predictive Engine Monitoring

This is an MVP of a predictive maintenance system for marine and automotive engines. It uses an AI model to analyze vibration data and detect the early signs of mechanical failure.

## How to Use This Demo

1.  **Get Sample Data:** You can copy the sample data from the `data/raw_data.csv` file in the repository. You will need at least 51 rows.
2.  **Paste Data:** Paste the copied CSV data into the input box.
3.  **Get Prediction:** The model will analyze the last sequence of data and determine if it represents a "Normal" or "Anomalous" engine state.
