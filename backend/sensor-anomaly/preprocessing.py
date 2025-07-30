import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Load the sensor data with explicit data types
df = pd.read_csv("sensor_data.csv", dtype=str)  # Read everything as strings first

# Convert timestamp column to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')

# Clean and convert numeric columns
numeric_columns = ["humidity", "temperature", "soil_sensor_1", "soil_sensor_2"]

for col in numeric_columns:
    df[col] = df[col].astype(str).str.replace('%', '', regex=True)  # Remove percentage signs if present
    df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to float

# Handle missing values (replace NaN with median values)
df.fillna(df.median(numeric_only=True), inplace=True)

# Convert categorical columns to numeric (if needed)
df["motor_status"] = df["motor_status"].map({"On": 1, "Off": 0})
df["flame_detected"] = df["flame_detected"].map({"Yes": 1, "No": 0})

# Normalize numerical sensor values
scaler = MinMaxScaler()
df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

# Save preprocessed data
df.to_csv("preprocessed_sensor_data.csv", index=False)
print("Preprocessed data saved to preprocessed_sensor_data.csv")

# Show preview of the processed data
print(df.head())
