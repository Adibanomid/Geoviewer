import React, { useState } from "react";
import FileUpload from "./components/FileUpload";
import MapView from "./components/MapView";
import LoginForm from "./components/LoginForm";
import "./App.css";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");

  const handleLoginSuccess = (accessToken) => {
    localStorage.setItem("token", accessToken);
    setToken(accessToken);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken("");
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
              <FileUpload token={token} />
            </div>
            <div className="map-section">
              <MapView token={token} />
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
