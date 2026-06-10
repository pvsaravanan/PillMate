# PillMate — Quick Start Guide

Get PillMate running locally in about 5 minutes.

---

## Prerequisites

1. **Python 3.11+** — [Download](https://www.python.org/downloads/)
2. **Node.js 18+** — [Download](https://nodejs.org/)
3. **MongoDB** — [Install Guide](#step-2-install-mongodb)
4. **Google Gemini API Key** — [Get Free Key](https://aistudio.google.com/app/apikey)

---

## Step 1: Get a Google Gemini API Key

1. Go to https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (starts with `AIzaSy...`)

The free tier provides 60 requests/minute and 1,500 requests/day.

---

## Step 2: Install MongoDB

### macOS
```bash
brew tap mongodb/brew
brew install mongodb-community@7.0
brew services start mongodb-community@7.0
```

### Ubuntu / Linux
```bash
sudo apt-get install -y mongodb
sudo systemctl start mongodb
```

### Windows
Download from [mongodb.com](https://www.mongodb.com/try/download/community) and install.

**Verify it's running:**
```bash
mongosh
```

---

## Step 3: Set Up the Backend

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
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
GEMINI_API_KEY=YOUR_KEY_HERE
```

> Replace `YOUR_KEY_HERE` with your actual Gemini API key.

**Start the backend:**
```bash
uvicorn server:app --reload --port 8001
```

Backend running at http://localhost:8001

---

## Step 4: Set Up the Frontend

Open a **new terminal**:

```bash
cd frontend

# Install dependencies
npm install
```

**Create `frontend/.env`** (if it doesn't already exist):
```
REACT_APP_BACKEND_URL=http://localhost:8001
WDS_SOCKET_PORT=0
```

**Start the frontend:**
```bash
npm start
```

Frontend running at http://localhost:3000

---

## Done!

Open http://localhost:3000 to see the PillMate homepage.

### Quick Test
1. Click **Upload Prescription**
2. Choose a prescription image
3. Select your preferred language
4. Click **Analyze**
5. View AI-extracted medications with plain-language explanations

---

## Troubleshooting

### "GEMINI_API_KEY not found"
- Confirm `backend/.env` exists and contains the key
- No quotes around the key value
- Restart the backend after changes

### "Can't connect to MongoDB"
```bash
# Check if running
mongosh

# Start if needed
brew services start mongodb-community    # macOS
sudo systemctl start mongodb             # Linux
net start MongoDB                        # Windows
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

### "Module not found"
```bash
# Backend
cd backend && pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

---

## Files You'll Create

| File | Contents |
|---|---|
| `backend/.env` | API key, MongoDB URL, CORS config |
| `frontend/.env` | Backend URL |

**Never commit `.env` files to Git.**

---

## Stop Servers

Press `Ctrl+C` in each terminal.

---

## Checklist

- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] MongoDB running
- [ ] Gemini API key obtained
- [ ] `backend/.env` created
- [ ] `frontend/.env` created
- [ ] Backend running on port 8001
- [ ] Frontend running on port 3000
- [ ] Can upload prescriptions

---

## More Documentation

- Detailed setup: [LOCAL_SETUP.md](LOCAL_SETUP.md)
- Architecture: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Features: [docs/FEATURES.md](docs/FEATURES.md)
- Algorithms: [docs/ALGORITHMS.md](docs/ALGORITHMS.md)
