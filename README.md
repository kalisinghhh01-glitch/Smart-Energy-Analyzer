# ⚡ Smart Energy Analyzer

An AI-Based Smart Electrical Consumption Analyzer built using **C++ and Python** with an interactive Streamlit dashboard.

## 📌 Project Overview

Smart Energy Analyzer helps users monitor electricity consumption, estimate monthly bills, analyze appliance-wise energy usage, predict future consumption, and generate downloadable reports.

## ✨ Features

- Add, view and delete electrical appliances
- Calculate monthly electricity consumption in kWh
- Estimate electricity bills using sample tariff rates
- Analyze energy usage levels (Low, Medium, High)
- Identify the highest energy-consuming appliance
- Predict next month's consumption using average readings
- Generate downloadable energy reports
- Store appliance data using file handling

## 🛠️ Technologies Used

- C++ — Core calculations and energy analysis
- Python — Dashboard integration
- Streamlit — Interactive web interface
- Pandas — Data handling
- File Handling — Local data storage

## 🚀 How to Run

1. Clone or download this repository.
2. Open the project folder in VS Code.
3. Build the C++ engine:

   ```powershell
   .\build.bat
   ```

4. Install Python dependencies:

   ```powershell
   py -m pip install -r requirements.txt
   ```

5. Launch the dashboard:

   ```powershell
   py -m streamlit run app.py
   ```

6. Open the local URL displayed in the terminal.

## 📊 Bill Calculation

Monthly Energy (kWh):

`Quantity × Power (W) × Hours per Day × 30 / 1000`

The electricity tariff used is a sample academic tariff and may differ from actual electricity rates.

## 🔮 Prediction

The project uses a simple average of previous and current consumption readings to estimate next month's energy usage.

## 🎓 Project Information

**Project:** AI-Based Smart Electrical Consumption Analyzer

**Level:** First-Year Engineering Project

**Programming Language:** C++

**Dashboard:** Python + Streamlit

---

Developed as an academic engineering project.