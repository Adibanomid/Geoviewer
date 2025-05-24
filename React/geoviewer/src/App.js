import React, { useState } from "react";
import FileUpload from "./components/FileUpload";
import MapView from "./components/MapView";
import LoginForm from "./components/LoginForm";
import FileList from "./components/FileList";
import "./App.css";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [selectedFile, setSelectedFile] = useState(null);
  const [refreshFiles, setRefreshFiles] = useState(0);

  const handleLoginSuccess = (accessToken) => {
    localStorage.setItem("token", accessToken);
    setToken(accessToken);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken("");
  };

  const handleUploadSuccess = () => {
    setRefreshFiles((prev) => {
      console.log("Toggling refreshFiles:", prev + 1);
      return !prev;
    });
  };

  const handleFileSelect = (filename) => {
    setSelectedFile(filename);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h2>GeoTIFF Uploader</h2>
        {token && (
          <button className="logout-button" onClick={handleLogout}>
            Logout
          </button>
        )}
      </header>

      <main className="app-main">
        {!token ? (
          <LoginForm onLogin={handleLoginSuccess} />
        ) : (
          <>
            <div className="upload-section">
              <FileUpload token={token} onUploadSuccess={handleUploadSuccess} />
              <FileList
                token={token}
                onSelectFile={handleFileSelect}
                refresh={refreshFiles}
              />
            </div>
            <div className="map-section">
              <MapView filename={selectedFile} />
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
