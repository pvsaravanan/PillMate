# PillMate — Local Setup Guide

Detailed instructions for running PillMate on your local machine.

---

## Prerequisites

| Requirement | Minimum Version | Download |
|---|---|---|
| Python | 3.11+ | [python.org](https://www.python.org/downloads/) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org/) |
| MongoDB | 7.0 | [mongodb.com](https://www.mongodb.com/try/download/community) |
| Google Gemini API Key | — | [aistudio.google.com](https://aistudio.google.com/app/apikey) |

---

## Step-by-Step Setup

### 1. Get Your Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (starts with `AIza...`)

> **Important**: Keep this key secure and never commit it to version control.

---

### 2. Install MongoDB

#### macOS
```bash
brew tap mongodb/brew
brew install mongodb-community@7.0
brew services start mongodb-community@7.0
```

#### Ubuntu / Debian
```bash
sudo apt-get install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

#### Windows
1. Download from the [MongoDB Download Center](https://www.mongodb.com/try/download/community)
2. Install and start the MongoDB service

#### Verify MongoDB is running
```bash
mongosh
# Should connect successfully
```

---

### 3. Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Create a Python virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

**Create `backend/.env`:**
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=pillguide_local
CORS_ORIGINS=http://localhost:3000
GEMINI_API_KEY=YOUR_GOOGLE_GEMINI_API_KEY_HERE
```

> Replace `YOUR_GOOGLE_GEMINI_API_KEY_HERE` with your actual API key.

**Start the backend server:**
```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

Backend available at http://localhost:8001

---

### 4. Frontend Setup

Open a **new terminal window**:

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install
```

**Create or update `frontend/.env`:**
```
REACT_APP_BACKEND_URL=http://localhost:8001
WDS_SOCKET_PORT=0
```

**Start the frontend server:**
```bash
npm start
```

Frontend available at http://localhost:3000

---

## Testing the Application

### 1. Test the Backend API
```bash
curl http://localhost:8001/api/
```
Expected response:
```json
{"message": "PillMate API - Multi-Language Prescription System"}
```

### 2. Test the Frontend
Open http://localhost:3000 in your browser. You should see the PillMate homepage.

### 3. Test Prescription Upload
1. Click **Upload Prescription**
2. Select a prescription image
3. Choose your preferred language
4. Click **Analyze Prescription**
5. View extracted medications with explanations

---

## Project Structure

```
PillMate/
├── backend/
│   ├── server.py          # Main FastAPI application
│   ├── requirements.txt   # Python dependencies
│   ├── .env               # Backend environment variables (not committed)
│   └── venv/              # Python virtual environment
│
├── frontend/
│   ├── src/
│   │   ├── App.js         # Main React component & routing
│   │   ├── pages/         # Page components
│   │   └── components/    # UI components
│   ├── public/            # Static assets
│   ├── package.json       # Node dependencies
│   ├── craco.config.js    # CRACO build configuration
│   ├── .env               # Frontend environment variables
│   └── node_modules/      # Installed packages
│
├── docs/                  # Documentation
└── README.md              # Project overview
```

---

## Troubleshooting

### "GEMINI_API_KEY not found"
1. Ensure `backend/.env` exists
2. Verify the key is present: `GEMINI_API_KEY=AIza...`
3. No quotes around the value
4. Restart the backend server

### "MongoDB connection failed"
```bash
# Check if MongoDB is running
mongosh

# Start if needed
brew services start mongodb-community    # macOS
sudo systemctl start mongodb             # Linux
net start MongoDB                        # Windows
```

### "Module not found" errors
```bash
# Backend
cd backend
source venv/bin/activate    # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules
npm install
```

### "CORS errors" in the browser
Ensure `backend/.env` contains:
```
CORS_ORIGINS=http://localhost:3000
```

### "Port already in use"
```bash
# macOS / Linux
lsof -ti:8001 | xargs kill -9
lsof -ti:3000 | xargs kill -9

# Windows (PowerShell)
Stop-Process -Id (Get-NetTCPConnection -LocalPort 8001).OwningProcess -Force
Stop-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess -Force
```

---

## Development Workflow

### Making Changes

**Backend**: Edit `backend/server.py`. With the `--reload` flag, the server restarts automatically.

**Frontend**: Edit files under `frontend/src/`. The browser refreshes automatically via hot module replacement.

### Viewing Logs

- **Backend**: Check the terminal where `uvicorn` is running
- **Frontend**: Check the terminal where `npm start` is running, or open browser DevTools (F12)

---

## Database Access

```bash
# Connect to MongoDB
mongosh

# Switch to database
use pillguide_local

# View collections
show collections

# View prescriptions
db.prescriptions.find().pretty()

# View medications
db.medications.find().pretty()

# Clear all data (if needed)
db.prescriptions.deleteMany({})
db.medications.deleteMany({})
```

---

## Security Best Practices

1. **Never commit `.env` files** to Git
2. Add to `.gitignore`:
   ```
   .env
   venv/
   node_modules/
   ```
3. Keep API keys secure
4. Use environment variables for all sensitive data

---

## Building for Production

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8001 --workers 4
```

### Frontend
```bash
cd frontend
npm run build
# Deploy the build/ folder to your hosting service
```

---

## Common Commands Reference

### Start Everything
```bash
# Terminal 1 — Verify MongoDB
mongosh

# Terminal 2 — Backend
cd backend
source venv/bin/activate    # or venv\Scripts\activate on Windows
uvicorn server:app --reload --port 8001

# Terminal 3 — Frontend
cd frontend
npm start
```

### Stop Everything
Press `Ctrl+C` in each terminal.

---

## Verification Checklist

- [ ] MongoDB installed and running
- [ ] Google Gemini API key obtained
- [ ] `backend/.env` created with `GEMINI_API_KEY`
- [ ] Python dependencies installed
- [ ] Backend server running on port 8001
- [ ] `frontend/.env` created with `REACT_APP_BACKEND_URL`
- [ ] Node dependencies installed
- [ ] Frontend server running on port 3000
- [ ] Can access http://localhost:3000
- [ ] Can upload and analyze prescription images
