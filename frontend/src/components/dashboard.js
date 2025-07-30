import React, { useState, useEffect } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import Sidebar from "../components/sidebar"; // Import Sidebar Component
import "./dashboard.css"; // Import Dashboard styles

// Register chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const Dashboard = () => {
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false); // Sidebar state

  useEffect(() => {
    // Simulate data fetching
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  }, []);

  // Function: Toggle Sidebar
  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  // Dummy data for charts
  const labels = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"];
  const temperatureData = [22, 24, 23, 26, 27];
  const humidityData = [60, 62, 58, 64, 66];
  const rainfallData = [5, 10, 0, 20, 15];
  const soilMoisture1Data = [30, 35, 33, 37, 40];
  const soilMoisture2Data = [32, 34, 36, 38, 39];
  const nitrogenData = [10, 12, 11, 14, 13];
  const phosphorusData = [8, 9, 7, 10, 9];
  const potassiumData = [15, 16, 14, 17, 16];

  // Prepare data for charts
  const temperatureHumidityData = {
    labels,
    datasets: [
      {
        label: "Temperature (°C)",
        data: temperatureData,
        fill: false,
        borderColor: "rgb(75, 192, 192)",
      },
      {
        label: "Humidity (%)",
        data: humidityData,
        fill: false,
        borderColor: "rgb(153, 102, 255)",
      },
    ],
  };

  const rainfallDataChart = {
    labels,
    datasets: [
      {
        label: "Rainfall (mm)",
        data: rainfallData,
        fill: false,
        borderColor: "rgb(54, 162, 235)",
      },
    ],
  };

  const soilMoistureData = {
    labels,
    datasets: [
      {
        label: "Soil Moisture Sensor 1 (%)",
        data: soilMoisture1Data,
        fill: false,
        borderColor: "rgb(255, 99, 132)",
      },
      {
        label: "Soil Moisture Sensor 2 (%)",
        data: soilMoisture2Data,
        fill: false,
        borderColor: "rgb(255, 159, 64)",
      },
    ],
  };

  const npkData = {
    labels,
    datasets: [
      {
        label: "Nitrogen (N)",
        data: nitrogenData,
        fill: false,
        borderColor: "rgb(75, 192, 192)",
      },
      {
        label: "Phosphorus (P)",
        data: phosphorusData,
        fill: false,
        borderColor: "rgb(153, 102, 255)",
      },
      {
        label: "Potassium (K)",
        data: potassiumData,
        fill: false,
        borderColor: "rgb(255, 205, 86)",
      },
    ],
  };

  return (
    <div className="dashboard-container">
      <Sidebar sidebarOpen={sidebarOpen} toggleSidebar={toggleSidebar} /> {/* Include Sidebar */}
      <div className={`dashboard-content ${sidebarOpen ? 'sidebar-open' : ''}`}>
        <button className="burger" onClick={toggleSidebar}>☰</button> {/* Burger Menu Button */}
        <h2>Dashboard</h2>

        {loading && <p>Loading data...</p>}

        {!loading && (
          <div>
            <h3>Sensor Readings</h3>
            <p>🌡️ Temperature: {temperatureData[temperatureData.length - 1]}°C</p>
            <p>💧 Humidity: {humidityData[humidityData.length - 1]}%</p>
            <p>🌧️ Rainfall: {rainfallData[rainfallData.length - 1]} mm</p>
            <p>🌱 Soil Moisture Sensor 1: {soilMoisture1Data[soilMoisture1Data.length - 1]}%</p>
            <p>🌱 Soil Moisture Sensor 2: {soilMoisture2Data[soilMoisture2Data.length - 1]}%</p>
            <p>🧪 Nitrogen: {nitrogenData[nitrogenData.length - 1]}</p>
            <p>🧪 Phosphorus: {phosphorusData[phosphorusData.length - 1]}</p>
            <p>🧪 Potassium: {potassiumData[potassiumData.length - 1]}</p>

            <h3>Temperature and Humidity Trends</h3>
            <Line data={temperatureHumidityData} />

            <h3>Rainfall Trends</h3>
            <Line data={rainfallDataChart} />

            <h3>Soil Moisture Trends</h3>
            <Line data={soilMoistureData} />

            <h3>NPK Trends</h3>
            <Line data={npkData} />
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;