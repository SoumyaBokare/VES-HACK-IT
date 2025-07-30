from flask import Flask, request, jsonify
import joblib
import pandas as pd
import requests
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Load trained model
model = joblib.load("random_forest_model.pkl")

# OpenWeather API Key
API_KEY = "c04b996b12e5e232032b86822d8d1702"

# Initialize Firebase
cred = credentials.Certificate("finalparul-firebase-adminsdk-73r75-46bbe516c4.json")  # Replace with Firebase JSON
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://your-firebase-database-url.firebaseio.com/"
})

@app.route("/recommend-crop", methods=["GET"])
def recommend_crop():
    city = request.args.get("city", "Mumbai")  # Default city is Mumbai

    # Fetch city coordinates from OpenWeather API
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},IN&limit=1&appid={API_KEY}"
    geo_response = requests.get(geo_url).json()
    
    if not geo_response:
        return jsonify({"error": "City not found"}), 400

    lat, lon = geo_response[0]["lat"], geo_response[0]["lon"]

    # Fetch real-time rainfall data
    URL = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(URL)
    data = response.json()
    rainfall = data.get("rain", {}).get("1h", 0)

    # Fetch latest sensor data from Firebase
    ref = db.reference("sensor_data")
    sensor_data = ref.get()
    latest_sensor = list(sensor_data.values())[-1]

    # Dummy NPK values
    npk_values = {"Nitrogen": 50, "Phosphorus": 30, "Potassium": 20}

    # Combine all inputs
    input_data = {
        "temperature": latest_sensor["temperature"],
        "humidity": latest_sensor["humidity"],
        "soil_moisture_1": latest_sensor["soil_sensor_1"],
        "soil_moisture_2": latest_sensor["soil_sensor_2"],
        "ph": latest_sensor["ph"],  # Fetch pH value from Firebase
        "rainfall": rainfall,
        "Nitrogen": npk_values["Nitrogen"],
        "Phosphorus": npk_values["Phosphorus"],
        "Potassium": npk_values["Potassium"]
    }

    # Convert to DataFrame for model prediction
    input_df = pd.DataFrame([input_data])

    # Predict best crop
    predicted_crop = model.predict(input_df)[0]

    return jsonify({"recommended_crop": predicted_crop, "city": city})

if __name__ == "__main__":
    app.run(debug=True, port=5003)
