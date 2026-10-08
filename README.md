# Maritime Anomaly Detection — Visual Analytics

Interactive visual analytics system for exploring maritime vessel tracks from **AIS** and **radar** sources, detecting spatial/temporal anomalies (Hausdorff distance), clustering vessel behavior, and classifying radar tracks with machine learning.

## Features

- **Map explorer** (`/`) — Leaflet map of AIS and radar trajectories with date range, confidence, MMSI search, vessel-type filters, and Hausdorff-based anomaly highlighting
- **Cluster analysis** (`/clusters`) — t-SNE / feature exploration with K-Means and BMM clusters, radar charts, and AdaBoost / Gradient Boosting vessel-type prediction
- **Dashboard** (`/dashboard`) — aggregate charts over clustered track features (speed, curviness, heading, etc.)

## Architecture

| Layer | Stack | Port |
|-------|--------|------|
| Frontend | React 18, MUI, D3, Leaflet, Recharts | `3000` |
| Data API | Node.js, Express, Mongoose | `5000` |
| ML API | Flask, scikit-learn (`.pkl` models) | `5001` |
| Database | MongoDB (`viz_project`) | `27017` |

```
Browser (React)
    ├──► Express API  ──► MongoDB (ais, radar)
    └──► Flask /predict ──► AdaBoost / Gradient Boosting models
```

## Prerequisites

- [Node.js](https://nodejs.org/) (v16+ recommended)
- [MongoDB](https://www.mongodb.com/) running locally on `27017`
- [Python](https://www.python.org/) 3.8+ (for the ML service)
- npm

## Setup

### 1. Clone and install dependencies

```bash
# Backend (repo root)
npm install

# Frontend
cd front-end/anomaly-detection-frontend
npm install
cd ../..
```

### 2. Import data into MongoDB

Ensure MongoDB is running, then from the `raw data` folder:

```bash
cd "raw data"
pip install pymongo
python MongoDBImport.py
```

This loads:

- `26_2023_01_tracks_ais_simplified_2_wid.json` → collection `ais`
- `26_2023_01_tracks_radar_simplified_with_husdroff.json` → collection `radar`

into the `viz_project` database.

### 3. ML service dependencies

```bash
pip install flask flask-cors numpy scikit-learn
```

Models live in `ML_Model/`:

- `adaBoosting.pkl`
- `gradientBoosting.pkl`

## Running the application

Start all three services (separate terminals):

**1. MongoDB** (if not already running)

```bash
# Windows example
net start MongoDB
```

**2. Express data API**

```bash
npm start
# → http://localhost:5000
```

**3. Flask ML API**

```bash
python backend_ML.py
# → http://localhost:5001
```

**4. React frontend**

```bash
cd front-end/anomaly-detection-frontend
npm start
# → http://localhost:3000
```

## Pages

| Route | Description |
|-------|-------------|
| `/` | Interactive map of AIS/radar tracks and anomaly filters |
| `/clusters` | Cluster exploration and ML vessel-type classification |
| `/dashboard` | Summary visualizations of clustered track metrics |

## API overview

### Express (`:5000`)

- `POST /api/getdata/mongo` — radar tracks filtered by date, confidence, Hausdorff threshold, track limit
- `POST /api/getais/` — AIS tracks with similar filters
- Additional helpers for MMSI lookup, confidence histograms, and counts by vessel type

### Flask (`:5001`)

- `GET /` — health check
- `POST /predict` — body: `{ "features": [...], "algorithm": "adaboost" | "gboost" }`  
  Returns predicted vessel class and class probabilities:
  - Cargo Ships
  - Support, Utility, and Military Vessels
  - Passenger, Recreational, and Others

## Project structure

```
Anomaly-detection/
├── server.js                 # Express entry point
├── backend_ML.py             # Flask prediction service
├── package.json
├── models/
│   ├── ais.js                # Mongoose AIS schema
│   └── radar.js              # Mongoose radar schema
├── routes/
│   ├── getAIS.js             # AIS API routes
│   └── getData.js            # Radar / anomaly API routes
├── ML_Model/
│   ├── adaBoosting.pkl
│   ├── gradientBoosting.pkl
│   └── gradientBoosting.onnx
├── raw data/
│   ├── MongoDBImport.py
│   └── *.json                # Source track datasets
├── data/                     # Sample / legacy radar JSON
└── front-end/anomaly-detection-frontend/
    └── src/
        ├── App.js            # Map page
        ├── pages/
        │   ├── Clusters.js
        │   └── Dashboard.js
        ├── Components/       # Sidebar, charts, filters
        └── rawdata/          # CSV features for cluster views
```

## Configuration notes

- CORS on the Express server allows `http://localhost:3000`.
- MongoDB connection string defaults to `mongodb://127.0.0.1:27017/viz_project` in `server.js`.
- Map tiles use [Stadia Maps](https://stadiamaps.com/) Alidade Smooth Dark.

## Tech stack summary

**Frontend:** React, React Router, Material UI, D3.js, Leaflet / leaflet-draw, Recharts, react-dnd  

**Backend:** Express, Mongoose, MongoDB  

**ML:** Flask, scikit-learn (AdaBoost, Gradient Boosting), NumPy
```