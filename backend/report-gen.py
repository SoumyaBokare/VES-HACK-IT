import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import matplotlib.pyplot as plt
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os

class CropRecommendationSystem:
    def __init__(self, credentials_path, database_url):
        # Verify if the credentials file exists before initializing Firebase
        if not os.path.exists(credentials_path):
            raise FileNotFoundError(f"Firebase credentials file not found: {credentials_path}")
        
        # Initialize Firebase Admin SDK (Prevent multiple initializations)
        if not firebase_admin._apps:
            cred = credentials.Certificate(credentials_path)
            firebase_admin.initialize_app(cred, {'databaseURL': database_url})
        
        # Create output directory if it doesn't exist
        self.output_dir = r"C:\Users\soumy\OneDrive\Desktop\TY\HACKATHONS\VESIT\output"
        os.makedirs(self.output_dir, exist_ok=True)

    def fetch_sensor_data_from_firebase(self):
        # Attempt fetching data from multiple possible Firebase paths
        paths_to_try = [
            'sensor_data/latest_reading',
            'sensorData/latestReading',
            'sensor_data',
            'latest_reading'
        ]
        for path in paths_to_try:
            try:
                ref = db.reference(path)
                data = ref.get()
                if data:
                    return data
            except Exception as e:
                print(f"Error fetching from path {path}: {e}")
                continue

        # Default fallback if no data is found
        return {
            "Soil Moisture": "45%",
            "Temperature": "25°C",
            "Humidity": "60%",
            "timestamps": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        }

    def generate_graph(self, sensor_data):
        try:
            # Generate a simple graph
            times = sensor_data.get("timestamps", [datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            moisture_values = [float(str(sensor_data.get("Soil Moisture", "50%"))[:-1])]
            
            plt.figure(figsize=(6, 4))
            plt.plot(times, moisture_values, marker='o', linestyle='-', color='b', label='Soil Moisture (%)')
            plt.xlabel('Time')
            plt.ylabel('Soil Moisture (%)')
            plt.title('Soil Moisture Over Time')
            plt.xticks(rotation=30, ha='right')
            plt.grid(True)
            plt.legend()
            
            # Save the graph to a BytesIO object instead of a file
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png')
            plt.close()
            img_buffer.seek(0)
            return img_buffer
        except Exception as e:
            print(f"Error generating graph: {e}")
            return None

    def generate_pdf_report(self, sensor_data, recommendation):
        pdf_filename = os.path.join(self.output_dir, "crop_recommendation_report.pdf")
        print(f"📄 Generating PDF Report at: {pdf_filename}")

        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(pdf_filename), exist_ok=True)

            doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
            styles = getSampleStyleSheet()
            content = []

            # Add title
            content.append(Paragraph("Crop Recommendation Report", styles['Title']))
            content.append(Spacer(1, 12))

            # Create sensor data table
            cleaned_sensor_data = {
                k: v for k, v in sensor_data.items() 
                if k != 'timestamps' and not isinstance(v, (list, dict))
            }
            table_data = [["Parameter", "Value"]] + [
                [str(k), str(v)] for k, v in cleaned_sensor_data.items()
            ]
            
            table_style = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]
            table = Table(table_data)
            table.setStyle(table_style)
            content.append(table)
            content.append(Spacer(1, 12))

            # Add recommendation
            content.append(Paragraph("Recommendation:", styles['Heading2']))
            content.append(Paragraph(recommendation, styles['BodyText']))
            content.append(Spacer(1, 12))

            # Add graph
            graph_buffer = self.generate_graph(sensor_data)
            if graph_buffer:
                content.append(Image(graph_buffer, width=400, height=300))

            # Add timestamp
            content.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Italic']))
            
            # Build PDF
            doc.build(content)
            print(f"✅ PDF successfully saved at: {pdf_filename}")
            
            # Verify file was created
            if os.path.exists(pdf_filename):
                print(f"📄 PDF file size: {os.path.getsize(pdf_filename)} bytes")
            else:
                print("❌ PDF file was not created")
                
        except Exception as e:
            print(f"❌ Error generating PDF: {str(e)}")
            import traceback
            print(traceback.format_exc())

    def analyze_crop_recommendation(self, sensor_data):
        try:
            moisture_value = float(str(sensor_data.get("Soil Moisture", "50%"))[:-1])
            return ("Increase irrigation to maintain optimal moisture levels." if moisture_value < 50 
                    else "Soil moisture is adequate for current crop growth.")
        except Exception as e:
            print(f"Error analyzing crop recommendation: {e}")
            return "Unable to generate recommendation due to data issues."

    def run(self, num_reports=1):
        print("🔹 Running Crop Recommendation System...")
        try:
            sensor_data = self.fetch_sensor_data_from_firebase()
            print(f"✅ Sensor Data Retrieved: {sensor_data}")
            recommendation = self.analyze_crop_recommendation(sensor_data)
            print(f"💡 Recommendation: {recommendation}")
            self.generate_pdf_report(sensor_data, recommendation)
        except Exception as e:
            print(f"❌ Error in main run: {e}")
            import traceback
            print(traceback.format_exc())

if __name__ == "__main__":
    CREDENTIALS_PATH = r"C:\Users\soumy\OneDrive\Desktop\TY\HACKATHONS\VESIT\backend\finalparul-firebase-adminsdk-73r75-46bbe516c4.json"
    DATABASE_URL = 'https://finalparul-default-rtdb.asia-southeast1.firebasedatabase.app/'
    
    system = CropRecommendationSystem(CREDENTIALS_PATH, DATABASE_URL)
    system.run(num_reports=1)