---
title: PiranaWare Engine Diagnostics
emoji: 🛠️
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.29.0
app_file: app.py
pinned: false
---

# PiranaWare: Predictive Engine Diagnostics

This is an MVP of a predictive maintenance system for engines. It uses a regression-based AI model (XGBoost) to predict the normal vibration of an engine based on its current operating conditions.

## How to Use This Demo

1.  **Set Operating Conditions:** Use the sliders and dropdowns for input the engine's current RPM, the ambient temperature, fuel level, and sea state.
2.  **Enter Actual Vibration:** In the final box, enter the vibration reading you would get from a real-world sensor.
3.  **Get Prediction:** The model will compare the predicted "normal" vibration to the actual value and determine if it's an anomaly.

