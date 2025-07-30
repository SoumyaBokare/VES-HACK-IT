import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("finalparul-firebase-adminsdk-73r75-46bbe516c4.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://finalparul-default-rtdb.asia-southeast1.firebasedatabase.app/'})

# ✅ Fetch all sensor data
ref = db.reference('/sensor_data')
data = ref.get()

# ✅ Print the fetched data
print("Fetched Sensor Data:", data)
