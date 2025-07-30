import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Dashboard from "./components/dashboard";
import CropRec from "./components/crop-rec"; // Already handling city selection
import CropDisease from "./components/cropdisease";
import Anomaly from "./components/anomaly";
import ReportGeneration from "./components/report-gen";
import Settings from "./components/settings";
import Sidebar from "./components/sidebar"; // Ensure Sidebar remains

function App() {
  return (
    <Router>
      <Sidebar />
      <div style={{ marginLeft: "250px", padding: "20px" }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/crop-recommendation" element={<CropRec />} />
          <Route path="/crop-disease" element={<CropDisease />} />
          <Route path="/anomaly" element={<Anomaly />} />
          <Route path="/report-generation" element={<ReportGeneration />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
