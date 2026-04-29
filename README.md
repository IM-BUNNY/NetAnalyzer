# 🛡️ CyberSec Network Packet Analyzer — Project Report

## Overview
This full-stack cybersecurity application analyzes network traffic capture files (`.pcap`, `.pcapng`). It features a Python microservice using Scapy to dissect packets, a Node.js backend to manage uploads and coordinate analysis, and a stunning React frontend with a hacker-themed dashboard showing interactive intelligence. 

## Project Architecture & Folder Structure

```
CyberSec Project/
├── backend/
│   ├── package.json           # Node dependencies
│   ├── server.js              # Express API & Mongoose integration
│   ├── .env                   # Environment variables (Mongo URI)
│   ├── render.yaml            # Deployment config for Render
│   ├── uploads/               # Temporary storage for uploaded pcaps
│   └── parser/
│       ├── requirements.txt   # Python dependencies (Scapy)
│       └── analyzer.py        # Core packet dissection logic
│
└── frontend/
    ├── package.json           # React dependencies
    ├── vercel.json            # Deployment config for Vercel
    ├── tailwind.config.js     # Custom cyber-themed color palette
    ├── src/
    │   ├── main.jsx           # React entry point
    │   ├── index.css          # Global styles & Tailwind utilities
    │   └── App.jsx            # Main Dashboard & UI Components
```

## Step-by-Step Implementation Details

### Step 1 & 2: Packet Parsing Engine (Python + Scapy)
- **File**: `backend/parser/analyzer.py`
- **Functionality**: Reads `.pcap` files using `scapy`. 
- **Extraction**: Maps protocols (TCP, UDP, HTTP, DNS, ICMP), calculates total duration, monitors packet sizes, and establishes a timeline of packets/second.
- **Threat Detection**: Actively monitors for suspicious flags (e.g., high volumes of `SYN` packets indicating port scans) and traffic to notoriously vulnerable ports (e.g., 22 SSH, 3389 RDP, 445 SMB).
- **Output**: Dumps formatted JSON directly to `stdout` for the backend to capture.

### Step 3: API & Orchestration (Node.js + Express)
- **File**: `backend/server.js`
- **Functionality**: Serves the `/api/upload` and `/api/history` endpoints.
- **Workflow**:
  1. Accepts `.pcap` uploads via `multer`.
  2. Spawns a child process to run `python3 analyzer.py [file_path]`.
  3. Captures the JSON output.
  4. Saves the results to MongoDB for history tracking.
  5. Cleans up the uploaded file from the server.

### Step 4: The Cyber Dashboard (React + Tailwind + Chart.js)
- **File**: `frontend/src/App.jsx`
- **UI Design**: Inspired by elite cybersecurity tools (dark mode, monospace fonts, neon cyan/green/red accents, glassmorphism).
- **Components**:
  - **Uploader**: Drag-and-drop or click to upload target files.
  - **Live Terminal**: A scrolling log window showing real-time system actions and threat alerts.
  - **Metric Cards**: Total packets, capture duration, unique streams, and threat flags.
  - **Charts**: Doughnut chart for protocols, Bar chart for size distribution, Line chart for the network timeline.
  - **Top Talkers**: A table displaying the most active IP communication streams.

### Step 5: Database Integration (MongoDB)
- **Implementation**: Utilizes `mongoose` in the Node backend.
- **Functionality**: Automatically saves a summary of every analyzed file, including the timestamp and number of threats found. The frontend queries `/api/history` on load to fetch previous analysis records.

### Step 6: Deployment Strategy
- **Frontend (Vercel)**: `vercel.json` configures the build step and routes all traffic to `index.html` for client-side routing.
- **Backend (Render)**: `render.yaml` defines a web service that installs both Node (`npm install`) and Python (`pip install`) dependencies, ensuring the Express server and Scapy script can run harmoniously in the same container.

## Resume Bullet Points
You can add the following to your resume under "Projects":

* **Network Packet Analyzer (React, Node.js, Python, Scapy, MongoDB)**
  * Engineered a full-stack cybersecurity web app to parse and visualize `.pcap` network traffic data in real-time.
  * Built a Python microservice using Scapy to dissect packets, extracting protocol metrics and flagging malicious indicators (e.g., SYN port scans).
  * Designed an interactive, dark-themed React dashboard utilizing Chart.js for visualizing network topologies, timelines, and top-talker analytics.
  * Orchestrated seamless inter-process communication between Node.js Express backend and Python scripts, with MongoDB Atlas for persistence.

## How to Run Locally
1. Start the MongoDB service locally (or add `MONGO_URI` to `.env`).
2. Start backend: `cd backend && npm start` (Runs on port 5000)
3. Start frontend: `cd frontend && npm run dev` (Runs on port 5173)
