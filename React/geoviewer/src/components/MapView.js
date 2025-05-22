import React from "react";
import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export default function MapView() {
  return (
    <MapContainer
      center={[52.0, 9.0]} // Adjust based on your data location
      zoom={18} // Match zoom with your tile z
      style={{ height: "500px", width: "100%" }}
    >
      <TileLayer
        attribution="GeoTIFF Tiles"
        url="http://localhost:8000/api/tiles/GeogToWGS84GeoKey5.tif/{z}/{x}/{y}.png"
        tileSize={256}
        maxZoom={22}
        minZoom={0}
      />
    </MapContainer>
  );
}
