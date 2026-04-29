require('dotenv').config();
const express = require('express');
const cors = require('cors');
const multer = require('multer');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const mongoose = require('mongoose');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Ensure uploads directory exists
const uploadDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir);
}

// Multer config for file uploads
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/')
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + '-' + file.originalname)
    }
});
const upload = multer({ storage: storage });

// MongoDB Connection
// Set a fallback Mongo URI to use local DB if MONGO_URI is not set in .env
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/cybersec_analyzer';

mongoose.connect(MONGO_URI)
  .then(() => console.log('✅ Connected to MongoDB'))
  .catch(err => console.error('❌ MongoDB Connection Error:', err));

// Mongoose Schema for Analysis History
const analysisSchema = new mongoose.Schema({
    filename: String,
    timestamp: { type: Date, default: Date.now },
    summary: Object,
    threats_found: Number
});
const Analysis = mongoose.model('Analysis', analysisSchema);

// Routes
app.post('/api/upload', upload.single('pcapFile'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No file uploaded' });
    }

    const filePath = req.file.path;
    const pythonScript = path.join(__dirname, 'parser', 'analyzer.py');

    console.log(`[!] Starting analysis on ${req.file.originalname}`);

    // Call Python Script
    const pythonProcess = spawn('python3', [pythonScript, filePath]);

    let dataString = '';
    let errorString = '';

    pythonProcess.stdout.on('data', (data) => {
        dataString += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        errorString += data.toString();
        console.error(`[Python Error] ${data}`);
    });

    pythonProcess.on('close', async (code) => {
        // Clean up uploaded file
        fs.unlink(filePath, (err) => {
            if (err) console.error(`Failed to delete ${filePath}`, err);
        });

        if (code !== 0) {
            return res.status(500).json({ error: 'Analysis failed', details: errorString });
        }

        try {
            const result = JSON.parse(dataString);
            
            // Save to MongoDB
            const analysisRecord = new Analysis({
                filename: req.file.originalname,
                summary: result.summary,
                threats_found: result.threats ? result.threats.length : 0
            });
            await analysisRecord.save();
            console.log(`[+] Analysis saved to DB`);

            res.json(result);
        } catch (err) {
            console.error("Failed to parse Python output:", err);
            res.status(500).json({ error: 'Failed to parse analysis results', details: dataString });
        }
    });
});

app.get('/api/history', async (req, res) => {
    try {
        const history = await Analysis.find().sort({ timestamp: -1 }).limit(10);
        res.json(history);
    } catch (err) {
        res.status(500).json({ error: 'Failed to fetch history' });
    }
});

app.get('/', (req, res) => {
    res.send('Network Analyzer API Running');
});

app.listen(PORT, () => {
    console.log(`🚀 Server running on port ${PORT}`);
});
