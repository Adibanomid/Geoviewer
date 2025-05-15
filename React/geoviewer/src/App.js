import React from "react";
import FileUpload from "./components/FileUpload";
import MapView from "./components/MapView";

function App() {
  return (
    <div>
      <h2>GeoTIFF Uploader</h2>
      <FileUpload />
      <MapView />
    </div>
  );
}

export default App;
