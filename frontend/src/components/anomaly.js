import React, { useState, useEffect } from "react";
import axios from "axios";
import Sidebar from "./sidebar"; // Ensure Sidebar component is in the same directory

const AnomaliesTable = () => {
    const [anomalies, setAnomalies] = useState([]);
    const [sidebarOpen, setSidebarOpen] = useState(true);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const toggleSidebar = () => {
        setSidebarOpen(!sidebarOpen);
    };

    useEffect(() => {
        const fetchAnomalies = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:5004/anomalies");
                setAnomalies(response.data);
            } catch (err) {
                setError("Failed to fetch anomalies");
                console.error("Error fetching anomalies:", err);
            } finally {
                setLoading(false);
            }
        };

        fetchAnomalies();
    }, []);

    return (
        <div style={{ display: "flex" }}>
            {/* Sidebar Component */}
            <Sidebar sidebarOpen={sidebarOpen} toggleSidebar={toggleSidebar} />

            <div style={{ marginLeft: sidebarOpen ? "250px" : "0", transition: "margin-left 0.3s", padding: "20px", width: "100%" }}>
                <h2>Detected Sensor Anomalies</h2>
                {loading ? (
                    <p>Loading data...</p>
                ) : error ? (
                    <p>{error}</p>
                ) : anomalies.length === 0 ? (
                    <p>No anomalies detected ✅</p>
                ) : (
                    <table border="1" cellPadding="10" style={{ width: "100%", borderCollapse: "collapse" }}>
                        <thead>
                            <tr style={{ backgroundColor: "#f2f2f2" }}>
                                <th>Timestamp</th>
                                <th>Humidity</th>
                                <th>Temperature</th>
                                <th>Soil Sensor 1</th>
                                <th>Soil Sensor 2</th>
                                <th>Explanation</th>
                            </tr>
                        </thead>
                        <tbody>
                            {anomalies.map((anomaly, index) => (
                                <tr key={index}>
                                    <td>{anomaly.timestamp}</td>
                                    <td>{anomaly.humidity.toFixed(2)}</td>
                                    <td>{anomaly.temperature.toFixed(2)}</td>
                                    <td>{anomaly.soil_sensor_1.toFixed(2)}</td>
                                    <td>{anomaly.soil_sensor_2.toFixed(2)}</td>
                                    <td style={{ color: "red", fontWeight: "bold" }}>{anomaly.explanation}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
};

export default AnomaliesTable;