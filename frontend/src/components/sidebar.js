import React from "react";
import { useNavigate } from "react-router-dom";
import "./sidebar.css"; // Sidebar styles

const Sidebar = ({ sidebarOpen, toggleSidebar }) => {
  const navigate = useNavigate();
  return (
      <div className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
          <button className="close-btn" onClick={toggleSidebar}>×</button>
          <ul>
        <li onClick={() => navigate("/")}>🏠 Dashboard</li>
        <li onClick={() => navigate("/crop-recommendation")}>🌾 Crop Recommendation</li>
        <li onClick={() => navigate("/crop-disease")}>🦠 Crop Disease Detection</li>
        <li onClick={() => navigate("/anomaly")}>⚠️ Sensor Anomaly</li>
      </ul>
      </div>
  );
};
export default Sidebar;
