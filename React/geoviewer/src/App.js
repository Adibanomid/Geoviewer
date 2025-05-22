import React from "react";
import FileUpload from "./components/FileUpload";
import MapView from "./components/MapView";
import "./App.css";

function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h2>GeoTIFF Uploader</h2>
      </header>
      <main className="app-main">
        <div className="upload-section">
          <FileUpload />
        </div>
        <div className="map-section">
          <MapView />
        </div>
      </main>
    </div>
  );
}

export default App;
