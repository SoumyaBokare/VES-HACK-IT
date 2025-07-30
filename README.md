# VES-HACK-IT

A comprehensive agricultural solution combining crop recommendation, disease detection, and sensor anomaly detection to help farmers make informed decisions.

## Features

### 🌱 Crop Recommendation System
- Intelligent crop suggestions based on soil conditions, climate, and environmental factors
- Machine learning model trained on agricultural data
- Location-based recommendations

### 🔍 Crop Disease Detection
- AI-powered image analysis for crop disease identification
- Support for multiple disease types (Healthy, Powdery Mildew, Rust)
- Real-time disease classification using deep learning

### 📊 Sensor Anomaly Detection
- Monitor agricultural sensors for unusual readings
- Automatic anomaly detection and alerting
- Data visualization and reporting

### 📈 Dashboard & Analytics
- Comprehensive dashboard for monitoring all systems
- Generate detailed PDF reports
- Historical data analysis and trends

## Technology Stack

### Backend
- **Python Flask** - Web framework
- **TensorFlow/Keras** - Machine learning models
- **OpenCV** - Image processing
- **Firebase** - Database and authentication
- **Pandas/NumPy** - Data processing

### Frontend
- **React.js** - User interface
- **CSS3** - Styling
- **Chart.js** - Data visualization

## Project Structure

```
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── crop-rec.py           # Crop recommendation logic
│   ├── crop_disease.py       # Disease detection model
│   ├── sensor.py             # Sensor data processing
│   ├── report-gen.py         # PDF report generation
│   ├── models/               # Trained ML models
│   └── dataset/              # Training data
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   └── App.js           # Main application
│   └── public/              # Static assets
└── output/                  # Generated reports
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- Firebase account

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure Firebase:
   - Add your Firebase service account key as `finalparul-firebase-adminsdk-73r75-46bbe516c4.json`
   - Update `firebase-config.json` with your Firebase configuration

4. Run the Flask application:
   ```bash
   python app.py
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

## Usage

1. **Crop Recommendation**: Input soil parameters and location data to get crop suggestions
2. **Disease Detection**: Upload crop images to identify potential diseases
3. **Sensor Monitoring**: Connect agricultural sensors to monitor environmental conditions
4. **Reports**: Generate comprehensive PDF reports with analysis and recommendations

## API Endpoints

- `POST /crop-recommendation` - Get crop recommendations
- `POST /disease-detection` - Analyze crop images for diseases
- `GET /sensor-data` - Retrieve sensor readings
- `POST /generate-report` - Create PDF reports

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the agricultural research community for providing datasets
- TensorFlow and Keras teams for excellent ML frameworks
- React community for the robust frontend framework

## Contact

For questions or support, please open an issue in this repository.
