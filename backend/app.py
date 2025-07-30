import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import numpy as np
import io
import logging
import time
import json

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Flask Initialization
app = Flask(__name__)

# Enable CORS for all domains
CORS(app)

# Model and data paths
BASE_DIR = os.path.abspath(r"C:\Users\soumy\OneDrive\Desktop\TY\HACKATHONS\VESIT\backend\dataset")
MODEL_PATH = os.path.join(BASE_DIR, "final_model.keras")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Create static directory if it doesn't exist
os.makedirs(STATIC_DIR, exist_ok=True)

# Disease information
DISEASE_INFO = {
    "Healthy": {
        "description": "The plant appears healthy with no signs of disease.",
        "treatment": "Continue regular care, including appropriate watering, fertilization, and monitoring.",
        "prevention": "Maintain good growing conditions, proper spacing, and regular inspection."
    },
    "Powdery": {
        "description": "Powdery mildew appears as white or gray powdery spots on leaves, stems, and sometimes fruit.",
        "treatment": "Apply fungicides specifically designed for powdery mildew. Remove and destroy affected leaves.",
        "prevention": "Ensure good air circulation, avoid overhead watering, and keep plants spaced adequately."
    },
    "Rust": {
        "description": "Rust disease appears as orange, yellow, or brown pustules on the underside of leaves.",
        "treatment": "Apply appropriate fungicides. Remove and destroy infected plant parts.",
        "prevention": "Avoid wetting the foliage when watering, provide good air circulation, and use resistant varieties when available."
    }
}

# Check if the model file exists
if not os.path.exists(MODEL_PATH):
    logger.error(f"Model file not found at {MODEL_PATH}")
    exit(1)  # Exit if model file doesn't exist

# Load Pretrained Model
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    logger.info("Model loaded successfully!")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    exit(1)  # Exit if model loading fails

# Image Size for prediction
IMG_SIZE = (224, 224)

@app.route("/")
def index():
    return "Crop Disease Detection API is running!"

@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory(STATIC_DIR, filename)

@app.route("/health")
def health_check():
    return jsonify({"status": "ok", "timestamp": time.time()})

@app.route("/predict", methods=["POST"])
def predict():
    start_time = time.time()
    try:
        # Check if the image is part of the request
        if 'image' not in request.files:
            logger.warning("No image file provided in request")
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        
        # Debug: Print file info
        logger.info(f"File received: {file.filename}")
        logger.info(f"MIME type: {file.content_type}")
        
        # Ensure the file is an image based on extension and MIME type
        allowed_extensions = ('.png', '.jpg', '.jpeg')
        allowed_mime_types = ('image/png', 'image/jpeg', 'image/jpg')

        # Handle files from webcam that might not have an extension
        has_valid_extension = any(file.filename.lower().endswith(ext) for ext in allowed_extensions)
        has_valid_mime = file.content_type in allowed_mime_types
        
        if not has_valid_mime:
            logger.warning(f"Invalid MIME type: {file.content_type}")
            return jsonify({"error": "Invalid MIME type. Only PNG, JPG, and JPEG are allowed."}), 400
        
        if not has_valid_extension and has_valid_mime:
            # For webcam captures without extensions but with valid MIME types, continue processing
            logger.info("Processing webcam capture without extension")
        elif not has_valid_extension:
            logger.warning(f"Invalid file extension: {file.filename}")
            return jsonify({"error": "Invalid image file format. Only PNG, JPG, and JPEG are allowed."}), 400
        
        # Read the image file into memory
        img_bytes = file.read()
        
        # Process the image
        img = image.load_img(io.BytesIO(img_bytes), target_size=IMG_SIZE)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Rescale the image

        # Make the prediction
        prediction = model.predict(img_array)
        class_idx = np.argmax(prediction, axis=1)
        confidence = float(prediction[0][class_idx[0]])  # Get confidence score

        # Class Labels
        class_labels = {0: "Healthy", 1: "Powdery", 2: "Rust"}
        predicted_class = class_labels.get(class_idx[0], "Unknown")
        
        # Get disease information
        disease_info = DISEASE_INFO.get(predicted_class, {
            "description": "Information not available.",
            "treatment": "Consult with a plant specialist.",
            "prevention": "General good practices recommended."
        })
        
        # Log prediction results
        logger.info(f"Prediction: {predicted_class} with confidence {confidence:.4f}")
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Return the prediction result with additional info
        return jsonify({
            "prediction": predicted_class,
            "confidence": round(confidence * 100, 2),  # Convert to percentage
            "description": disease_info["description"],
            "treatment": disease_info["treatment"],
            "prevention": disease_info["prevention"],
            "processing_time_ms": round(processing_time * 1000, 2)
        })

    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}", exc_info=True)
        return jsonify({"error": f"Error in prediction: {str(e)}"}), 500

if __name__ == "__main__":
    logger.info(f"Starting Crop Disease Detection API on port 5004")
    app.run(debug=True, port=5004)