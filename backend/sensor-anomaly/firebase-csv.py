import firebase_admin
from firebase_admin import credentials, db
import pandas as pd

# Initialize Firebase Admin SDK
cred = credentials.Certificate("finalparul-firebase-adminsdk-73r75-46bbe516c4.json")  # Replace with your JSON file path
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://finalparul-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

# Reference the sensor data node in Firebase
ref = db.reference("sensor_data")

# Fetch data from Firebase
data = ref.get()

# Convert Firebase data to a Pandas DataFrame
sensor_records = []
for key, values in data.items():
    sensor_records.append({
        "timestamp": values.get("timestamp"),
        "humidity": values.get("humidity"),
        "temperature": values.get("temperature"),
        "soil_sensor_1": values.get("soil_sensor_1"),
        "soil_sensor_2": values.get("soil_sensor_2"),
        "motor_status": values.get("motor_status"),
        "flame_detected": values.get("flame_detected"),
    })

# Create DataFrame
df = pd.DataFrame(sensor_records)

# Save to CSV
df.to_csv("sensor_data.csv", index=False)
print("Sensor data saved to sensor_data.csv")
