import React from 'react';
import './sensor.css';

function SensorCard({ label, value, unit }) {
  return (
    <div className="sensor-card">
      <h3>{label}</h3>
      <p>{value} {unit}</p>
    </div>
  );
}

export default SensorCard;