import React, { useState } from "react";
import axios from "axios";

export default function FileUpload() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);
    try {
      await axios.post("http://localhost:8000/api/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage("Upload successful!");
    } catch (error) {
      setMessage("Upload failed!");
    }
  };

  return (
    <div>
      <input
        type="file"
        accept=".tif,.tiff"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button onClick={handleUpload}>Upload</button>
      <p>{message}</p>
    </div>
  );
}
