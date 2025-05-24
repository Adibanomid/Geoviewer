# GeoTIFF Uploader & Tile Server

## Overview

This project is a **GeoTIFF Upload and Tile Serving Web Application** built with **React** on the frontend and **Django + rio-tiler** on the backend. It allows users to:

- **Authenticate** with a secure login system (JWT-based).
- **Upload GeoTIFF files** via a web interface.
- **List available uploaded files** dynamically.
- **Visualize GeoTIFF data on an interactive Leaflet map** by selecting from the list.
- **Serve map tiles dynamically** from uploaded GeoTIFF files, allowing seamless zooming and panning.

---

## Features

- User authentication and session management.
- Upload GeoTIFF raster files securely.
- List and select uploaded GeoTIFFs to display as map layers.
- Backend tile rendering using `rio-tiler` for efficient on-demand tile generation.
- Frontend map visualization with Leaflet and React.
- Auto-refresh file list after new uploads.
- Error handling with clear feedback.

---

## Technologies Used

### Backend

- **Python 3.x**
- **Django 4.x** — Web framework for API and backend logic.
- **Django REST Framework** — For REST API endpoints.
- **rio-tiler** — Efficient tile serving for geospatial raster data.
- **rasterio** — Geospatial raster processing.
- **mercantile** — For XYZ tile scheme management.
- **PostgreSQL (optional)** — For user authentication and metadata storage.
- **JWT (JSON Web Tokens)** — Secure token-based authentication.

### Frontend

- **React 18.x** — UI Library.
- **Leaflet** — Interactive maps.
- **React-Leaflet** — React bindings for Leaflet.
- **Fetch API** — For communicating with backend APIs.
- **CSS Modules / SCSS** — Styling.

---

## Installation & Setup

### Prerequisites

- Python 3.8+ installed
- Node.js 16+ and npm/yarn installed
- PostgreSQL installed and configured (if used)
- Optional: virtual environment tool (e.g., `venv` or `virtualenv`)

---

### Backend Setup

```bash
# Create and activate virtual environment
python -m venv env
# On Linux/macOS:
source env/bin/activate
# On Windows:
env\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser (needed for login)
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

# Frontend Setup

```bash
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install
# or
yarn install

# Start frontend dev server
npm start
# or
yarn start
```

## Usage Guide

### User Authentication

- Access the frontend at `http://localhost:3000`.

- Login with your credentials or register if supported.

- Upon successful login, you get access to upload and view GeoTIFF files.

### Uploading Files

- Use the **Upload** section to select and upload GeoTIFF files.

- On upload success, the file list refreshes automatically.

### File List and Map View

- Available GeoTIFF files are listed on the left.

- Clicking a filename will load its tile layer onto the map.

- You can zoom and pan the map interactively.

### Tile Serving

- Tiles are served dynamically by the Django backend using the XYZ tiling scheme.

- Tiles are rendered on-demand from GeoTIFF data using `rio-tiler`.

---

## Troubleshooting

- **Invalid Token / Auth Errors**: Ensure your JWT token is valid and included in API requests.

- **Tile Rendering Errors (500)**: Check that GeoTIFF files have valid CRS metadata; files without CRS are assigned EPSG:4326 automatically.

- **File List Not Refreshing**: Ensure the frontend state refresh flag toggles after upload success.

- **Map Not Updating**: Verify the selected file name is passed correctly and tiles are requested properly.

---

## Future Improvements

- More advanced tile caching and performance optimizations.

- handling non cordinated tiff files(error message in front or assigning automatically)

- Support for user registration and password reset.

- Allow file deletion and management.

- Support for different CRS and reprojection on the fly.

- caching system to improve performance

- using celery for async upload and conversion

- docker files and docker compose to impliment on a host for live demo
