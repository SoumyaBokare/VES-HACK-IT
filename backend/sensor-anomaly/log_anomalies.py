import os
import pandas as pd
from sklearn.ensemble import IsolationForest
from flask import Flask, jsonify
from flask_cors import CORS

# Flask Initialization
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS) for frontend requests

# Load the preprocessed sensor data
try:
    df = pd.read_csv("./preprocessed_sensor_data.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    print("✅ Sensor Data Loaded Successfully")
except Exception as e:
    print(f"❌ Error loading sensor data: {str(e)}")
    df = pd.DataFrame()

# Verify the columns and ensure that the expected columns exist
print("Columns in the DataFrame:", df.columns)

# Clean up column names by stripping spaces, only for string columns
df.columns = [str(col).strip() for col in df.columns]

# Now we will only keep these columns since NPK sensors are removed
sensor_columns = ["humidity", "temperature", "soil_sensor_1", "soil_sensor_2"]

# Ensure that these columns are in the data before processing
missing_columns = [col for col in sensor_columns if col not in df.columns]
if missing_columns:
    print(f"❌ Missing columns: {missing_columns}")
    # If any columns are missing, you can fill them with default values or handle accordingly
    for col in missing_columns:
        df[col] = 0  # You can fill with zeros or any default value you'd like

# Check if DataFrame is empty or if no data is available
if df.empty or df[sensor_columns].isnull().all().all():
    print("❌ No data available for anomaly detection.")
else:
    # Apply Isolation Forest to detect anomalies
    iso_forest = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    df["anomaly"] = iso_forest.fit_predict(df[sensor_columns])

    # Extract anomalies
    anomalies = df[df["anomaly"] == -1].reset_index()

    # Function to generate explanations for detected anomalies
    def get_anomaly_reason(row):
        if row["soil_sensor_1"] > 0.9:
            return "Sudden spike in soil moisture detected."
        elif row["soil_sensor_2"] < 0.1:
            return "Soil moisture critically low."
        elif row["temperature"] > 0.8:
            return "High temperature detected."
        elif row["humidity"] < 0.2:
            return "Humidity levels too low."
        else:
            return "Unexpected sensor behavior detected."

    # Apply the explanation function
    anomalies["explanation"] = anomalies.apply(get_anomaly_reason, axis=1)

# Endpoint to fetch anomalies
@app.route("/anomalies", methods=["GET"])
def get_anomalies():
    try:
        if anomalies.empty:
            return jsonify({"error": "No anomalies detected"}), 404

        anomaly_records = anomalies[[
            "timestamp", "humidity", "temperature", "soil_sensor_1", 
            "soil_sensor_2", "explanation"
        ]].to_dict(orient="records")
        return jsonify(anomaly_records)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch anomalies: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5004)
