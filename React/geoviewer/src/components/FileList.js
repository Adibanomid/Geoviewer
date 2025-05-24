import React, { useState, useEffect } from "react";
import "./FileList.css";

function FileList({ onSelectFile, refresh, token }) {
  const [files, setFiles] = useState([]);

  useEffect(() => {
    console.log("Refreshing file list...");
    fetch("http://localhost:8000/api/files/", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("Files fetched:", data);
        setFiles(data.files || []);
      })
      .catch((err) => {
        console.error("Failed to fetch files:", err);
      });
  }, [token, refresh]);

  return (
    <div className="file-list">
      <h3>Available GeoTIFF Files</h3>
      <ul>
        {files.length === 0 && <li>No files available</li>}
        {files.map((file) => (
          <li key={file}>
            <button onClick={() => onSelectFile(file)}>{file}</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default FileList;
