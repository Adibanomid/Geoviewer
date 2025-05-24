import React, { useState } from "react";
import axios from "axios";
import "./FileUpload.css";

export default function FileUpload({ onUploadSuccess, token }) {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState("");
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (e) => {
    setError("");
    setMessage("");
    setProgress(0);
    const selectedFile = e.target.files[0];

    if (!selectedFile) {
      setFile(null);
      return;
    }

    // File extension check
    if (!selectedFile.name.toLowerCase().match(/\.(tif|tiff)$/)) {
      setError("Only .tif or .tiff files are allowed.");
      setFile(null);
      return;
    }

    // MIME type check
    const validTypes = ["image/tiff", "image/x-tiff"];
    if (!validTypes.includes(selectedFile.type)) {
      setError("Invalid file type. Please upload a valid GeoTIFF.");
      setFile(null);
      return;
    }

    // Size limit check
    if (selectedFile.size > 500 * 1024 * 1024) {
      setError("File size exceeds 500MB limit.");
      setFile(null);
      return;
    }

    setFile(selectedFile);
    setMessage(`File ready to upload: ${selectedFile.name}`);
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      setIsUploading(true);
      setMessage("Uploading...");
      setError("");

      const response = await axios.post(
        "http://localhost:8000/api/upload/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${token}`,
          },
          onUploadProgress: (e) => {
            const percent = Math.round((e.loaded * 100) / e.total);
            setProgress(percent);
          },
        }
      );

      setIsUploading(false);
      setMessage("Upload successful!");
      setError("");
      setProgress(0);
      setFile(null);

      if (onUploadSuccess) {
        onUploadSuccess(response.data);
      }
    } catch (err) {
      console.error(err);
      setIsUploading(false);
      setProgress(0);
      setMessage("");

      // Try to extract backend validation error message(s)
      if (
        err.response &&
        err.response.data &&
        typeof err.response.data === "object"
      ) {
        const data = err.response.data;

        if (data.file && Array.isArray(data.file) && data.file.length > 0) {
          setError(`${data.file.join(" ")}`);
          return;
        }
      }

      // Fallback error message
      setError("Upload failed. Please try again.");
    }
  };

  return (
    <div className="file-upload">
      <input
        type="file"
        accept=".tif,.tiff"
        onChange={handleFileChange}
        className="file-input"
      />
      <button
        onClick={handleUpload}
        disabled={!file || isUploading || !!error}
        className={`upload-button ${isUploading || error ? "disabled" : ""}`}
      >
        {isUploading ? "Uploading..." : "Upload"}
      </button>

      {progress > 0 && (
        <div className="progress-wrapper">
          <p className="progress-text">Progress: {progress}%</p>
          <div className="progress-bar-bg">
            <div className="progress-bar" style={{ width: `${progress}%` }} />
          </div>
        </div>
      )}

      {message && <p className="success-message">{message}</p>}
      {error && <p className="error-message">{error}</p>}
    </div>
  );
}
