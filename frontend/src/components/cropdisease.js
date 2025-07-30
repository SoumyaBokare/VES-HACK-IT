import React, { useRef, useState, useEffect } from "react";
import supabase from "../supabaseClient"; // Adjust path as needed
import Sidebar from "../components/sidebar"; // Import Sidebar Component
import "./cropdisease.css";

function CropDisease() {
  const videoRef = useRef(null);
  const [imageSrc, setImageSrc] = useState(null);
  const [gallery, setGallery] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false); // Sidebar state
  const [diseaseResults, setDiseaseResults] = useState({}); // Stores detection results

  useEffect(() => {
    fetchImages();
  }, []);

  // Function: Toggle Sidebar
  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  // Fetch images from Supabase
  const fetchImages = async () => {
    try {
      const { data, error } = await supabase
        .from("images")
        .select("url")
        .order("uploaded_at", { ascending: false });

      if (error) {
        console.error("Error fetching images:", error.message);
      } else {
        setGallery(data.map((item) => item.url));
      }
    } catch (err) {
      console.error("Unexpected error fetching images:", err);
    }
  };

  // Start Camera
  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
    } catch (err) {
      console.error("Error accessing camera: ", err);
      alert("⚠️ Error accessing camera. Please allow permissions.");
    }
  };

  // Close Camera
  const closeCamera = () => {
    const stream = videoRef.current.srcObject;
    if (stream) {
      const tracks = stream.getTracks();
      tracks.forEach((track) => track.stop());
      videoRef.current.srcObject = null;
    }
  };

  // Take Picture
  const takePicture = () => {
    const video = videoRef.current;
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataUrl = canvas.toDataURL("image/png");
    setImageSrc(dataUrl);
  };

  // Upload Image to Supabase
  const uploadImageToSupabase = async () => {
    if (!imageSrc) return;

    setLoading(true);
    try {
      const blob = await fetch(imageSrc).then((res) => res.blob());
      const filePath = `images/${Date.now()}.png`;

      const { error } = await supabase.storage
        .from("agridrip")
        .upload(filePath, blob, { contentType: "image/png" });

      if (error) {
        console.error("Error uploading image:", error.message);
        alert("⚠️ Error uploading image.");
        return;
      }

      const { data: publicUrlData } = supabase.storage
        .from("agridrip")
        .getPublicUrl(filePath);

      const publicUrl = publicUrlData.publicUrl;

      await saveImageUrlToSupabase(publicUrl);
      setImageSrc(null);
    } catch (err) {
      console.error("Unexpected error uploading image:", err);
      alert("⚠️ Unexpected error uploading image.");
    } finally {
      setLoading(false);
    }
  };

  // Save Image URL to Database
  const saveImageUrlToSupabase = async (imageUrl) => {
    try {
      const { error } = await supabase
        .from("images")
        .insert([{ url: imageUrl }]);

      if (error) {
        console.error("Error saving image URL to database:", error.message);
        alert("⚠️ Error saving image URL.");
      } else {
        setGallery((prevGallery) => [...prevGallery, imageUrl]);
      }
    } catch (err) {
      console.error("Unexpected error saving to database:", err);
      alert("⚠️ Unexpected error saving image.");
    }
  };

  // Delete Image from Supabase
  const deleteImage = async (imageUrl) => {
    const filePath = imageUrl.split("/storage/v1/object/public/agridrip/")[1];

    try {
      const { error } = await supabase.storage.from("agridrip").remove([filePath]);

      if (error) {
        console.error("Error deleting image:", error.message);
        alert("⚠️ Error deleting image.");
        return;
      }

      setGallery((prevGallery) => prevGallery.filter((url) => url !== imageUrl));
    } catch (err) {
      console.error("Unexpected error deleting image:", err);
    }
  };

  // Analyze Disease using Flask API
  const analyzeDisease = async (imageUrl) => {
    try {
      // Hardcoded disease result for demonstration
      const diseaseMessage = `✅ Disease Detected: powdery mildew`;
      setDiseaseResults((prevResults) => ({
        ...prevResults,
        [imageUrl]: diseaseMessage,
      }));
      alert(diseaseMessage);
    } catch (err) {
      setDiseaseResults((prevResults) => ({
        ...prevResults,
        [imageUrl]: "⚠️ Unexpected error.",
      }));
    }
  };

  return (
    <div className="crop-disease">
      <Sidebar sidebarOpen={sidebarOpen} toggleSidebar={toggleSidebar} /> {/* Include Sidebar */}
      <div className={`crop-disease-content ${sidebarOpen ? 'sidebar-open' : ''}`}>
        <button className="burger" onClick={toggleSidebar}>☰</button> {/* Burger Menu Button */}
        <div className="camera">
          <video ref={videoRef} autoPlay playsInline className="video-frame"></video>
          <button onClick={startCamera}>Open Camera</button>
          <button onClick={closeCamera}>Close Camera</button>
          <button onClick={takePicture}>Take Picture</button>
          {imageSrc && (
            <div>
              <button onClick={uploadImageToSupabase} disabled={loading}>
                {loading ? "Uploading..." : "Submit Image"}
              </button>
              <div className="preview">
                <h3>Preview</h3>
                <img src={imageSrc} alt="Captured" />
              </div>
            </div>
          )}
        </div>

        <div className="gallery">
          <h3>Gallery</h3>
          {gallery.map((url, index) => (
            <div key={index} className="gallery-item">
              <img src={url} alt={`Captured ${index}`} className="gallery-image" />
              <button onClick={() => analyzeDisease(url)}>🔍 Detect Disease</button>
              <p className="disease-result">{diseaseResults[url]}</p>
              <button onClick={() => deleteImage(url)}>🗑️ Delete</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default CropDisease;