import React, { useState } from "react";
import Sidebar from "../components/sidebar"; // Ensure correct import

const CropRec = () => {
    const [selectedCity, setSelectedCity] = useState("Mumbai");
    const [recommendedCrop, setRecommendedCrop] = useState(null);
    const [additionalData, setAdditionalData] = useState({
        temperature: 26.0,
        humidity: 60,
        rainfall: 15,
    });
    const [sidebarOpen, setSidebarOpen] = useState(false); // Sidebar state

    const toggleSidebar = () => {
        setSidebarOpen(!sidebarOpen);
    };

    // Hardcoded crop details
    const cropDetails = {
        "Wheat": {
            image: "/images/wheat.jpeg",  // Store in public/images
            reason: "Wheat is recommended due to moderate temperature and low humidity, ideal for its growth."
        },
        "Rice": {
            image: "/images/rice.jpeg",  // Store in public/images
            reason: "High humidity and adequate rainfall make rice a perfect choice for this region."
        },
        "Maize": {
            image: "/images/corn.jpeg",  // Store in public/images
            reason: "Maize thrives in moderate rainfall and warm temperatures, suitable for this location."
        },
        "Cotton": {
            image: "/images/cotton.jpg",  // Store in public/images
            reason: "Cotton prefers dry climate with good soil moisture and moderate nitrogen levels."
        },
        "Sugarcane": {
            image: "https://upload.wikimedia.org/wikipedia/commons/7/79/Sugarcane_field.jpg",
            reason: "Sugarcane requires high water availability and humidity, which fits this environment."
        },
        "Pomegranate": {
            image: "https://upload.wikimedia.org/wikipedia/commons/b/bd/Pomegranate_fruit.JPG",
            reason: "This crop is drought-resistant and grows well in semi-arid conditions."
        },
        "Barley": {
            image: "https://upload.wikimedia.org/wikipedia/commons/1/1a/Barley_field.jpg",
            reason: "Barley thrives in cooler temperatures and requires moderate rainfall."
        },
        "Chickpea": {
            image: "https://upload.wikimedia.org/wikipedia/commons/4/4f/Chickpea_field.jpg",
            reason: "Chickpeas are well-suited for semi-arid regions with moderate temperatures."
        },
        "Tomato": {
            image: "https://upload.wikimedia.org/wikipedia/commons/9/9b/Tomato_je.jpg",
            reason: "Tomatoes require moderate temperature and sunlight, and are ideal for tropical climates."
        },
        "Potato": {
            image: "https://upload.wikimedia.org/wikipedia/commons/4/42/Potato_and_cross_section.jpg",
            reason: "Potatoes thrive in cooler climates with moderate humidity and adequate soil moisture."
        }
    };

    // Hardcoded list of cities (no need for API calls)
    const cities = [
        "Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad",
        "Solapur", "Amravati", "Kolhapur", "Thane", "Latur"
    ];

    // Handle city selection change
    const handleCityChange = (event) => {
        setSelectedCity(event.target.value);
    };

    // Fetch the recommended crop and data based on hardcoded logic
    const fetchCropRecommendation = () => {
        let crop = "Rice"; // Default crop, can be updated based on logic

        // Simple logic to recommend crops based on city (can be improved for real-world use)
        if (selectedCity === "Mumbai" || selectedCity === "Pune" || selectedCity === "Nagpur") {
            crop = "Rice";
        } else if (selectedCity === "Aurangabad" || selectedCity === "Solapur") {
            crop = "Cotton";
        } else if (selectedCity === "Amravati") {
            crop = "Pomegranate";
        } else {
            crop = "Maize";
        }

        setRecommendedCrop(crop);
        setAdditionalData({
            temperature: 28,
            humidity: 75,
            rainfall: 40,
        });
    };

    return (
        <div style={{ display: "flex" }}>
            <Sidebar sidebarOpen={sidebarOpen} toggleSidebar={toggleSidebar} />

            <div style={{ padding: "20px", maxWidth: "600px", margin: "auto", textAlign: "center", fontFamily: "Arial, sans-serif", marginLeft: sidebarOpen ? "250px" : "0", transition: "margin-left 0.3s" }}>
                {!sidebarOpen && (
                    <button
                        className="burger"
                        onClick={toggleSidebar}
                        style={{ position: "absolute", left: "10px", top: "10px", padding: "8px 12px", fontSize: "18px", cursor: "pointer" }}
                    >
                        ☰
                    </button>
                )}

                <h2>🌱 Crop Recommendation System</h2>

                {/* City Selection Dropdown */}
                <label style={{ fontWeight: "bold" }}>Select City: </label>
                <select value={selectedCity} onChange={handleCityChange} style={{ padding: "5px", marginLeft: "10px" }}>
                    {cities.map((city, index) => (
                        <option key={index} value={city}>
                            {city}
                        </option>
                    ))}
                </select>

                {/* Get Recommendation Button */}
                <button
                    onClick={fetchCropRecommendation}
                    style={{ marginLeft: "10px", padding: "8px 15px", backgroundColor: "#28a745", color: "white", border: "none", cursor: "pointer", borderRadius: "5px" }}
                >
                    Get Recommendation
                </button>

                <div style={{ marginTop: "20px", padding: "15px", border: "1px solid #ddd", borderRadius: "10px", backgroundColor: "#f9f9f9" }}>
                    <h3>🌾 Recommended Crop: <span style={{ color: "#28a745" }}>{recommendedCrop}</span></h3>

                    {cropDetails[recommendedCrop] && (
                        <img src={cropDetails[recommendedCrop].image} alt={recommendedCrop} style={{ width: "100%", maxHeight: "250px", borderRadius: "10px", marginTop: "10px" }} />
                    )}

                    {cropDetails[recommendedCrop] && (
                        <p style={{ fontStyle: "italic", marginTop: "10px" }}>{cropDetails[recommendedCrop].reason}</p>
                    )}

                    <h4>📊 Environmental Conditions</h4>
                    <p>🌡️ Temperature: <strong>{additionalData.temperature}°C</strong></p>
                    <p>💧 Humidity: <strong>{additionalData.humidity}%</strong></p>
                    <p>🌧️ Rainfall: <strong>{additionalData.rainfall}mm</strong></p>
                </div>
            </div>
        </div>
    );
};

export default CropRec;
