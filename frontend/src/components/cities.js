import React, { useState } from "react";

const SelectCity = ({ onCitySelect }) => {
    const cities = [
        "Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad",
        "Solapur", "Amravati", "Kolhapur", "Sangli", "Jalgaon",
        "Ahmednagar", "Latur", "Dhule", "Satara", "Chandrapur",
        "Parbhani", "Jalna", "Akola", "Nanded", "Ratnagiri"
    ];

    const [selectedCity, setSelectedCity] = useState("");

    const handleCityChange = (event) => {
        setSelectedCity(event.target.value);
        onCitySelect(event.target.value);
    };

    return (
        <div style={{ padding: "20px" }}>
            <label>Select City: </label>
            <select value={selectedCity} onChange={handleCityChange}>
                <option value="">-- Select a City --</option>
                {cities.map((city, index) => (
                    <option key={index} value={city}>
                        {city}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default SelectCity;
