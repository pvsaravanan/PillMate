# PillMate — Technical Documentation Index

## Documentation Overview

This directory contains comprehensive documentation for the PillMate prescription adherence management system.

---

## Documentation Files

### 1. ARCHITECTURE.md — System Architecture
Complete system design and technical architecture.

**Contents**: High-level architecture diagrams, component breakdown, technology stack details, data flow diagrams, AI integration architecture, security and privacy measures, performance considerations.

**Read this for**: Understanding how PillMate is built.

---

### 2. FEATURES.md — Feature Documentation
Detailed explanation of all application features.

**Contents**: Core features overview, multi-language support, behavioral science integration (Nudge Theory), safety features, user experience design, complete API reference, feature roadmap, success metrics.

**Read this for**: Understanding what PillMate does.

---

### 3. ALGORITHMS.md — Algorithms & Logic
Technical algorithms and implementation details.

**Contents**: Image analysis algorithm, language detection logic, JSON extraction algorithm, explanation generation, Nudge Theory engine, contraindication checking, Google Gemini integration, performance optimization, testing methodology.

**Read this for**: Understanding how features work internally.

---

### 4. MULTILANGUAGE_FEATURES.md — Multi-Language Guide
Comprehensive guide to multi-language support.

**Contents**: Supported languages (10+), how language detection works, translation system, dosage error prevention, cross-language examples, API endpoints, testing results, impact metrics.

**Read this for**: Understanding multi-language capabilities.

---

## Quick Start Guide

### For Developers

1. **Set up the backend**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   ```bash
   # backend/.env
   MONGO_URL=mongodb://localhost:27017
   DB_NAME=pillguide_local
   GEMINI_API_KEY=your_api_key_here
   CORS_ORIGINS=http://localhost:3000
   ```

3. **Start the backend**:
   ```bash
   uvicorn server:app --reload --port 8001
   ```

4. **Set up the frontend** (new terminal):
   ```bash
   cd frontend
   npm install
   npm start
   ```

5. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8001/api

### For Users
1. Upload a prescription (any language)
2. Select your preferred language for explanations
3. View medications with plain-language explanations
4. Check safety for drug interactions
5. Manage your medications list

---

## Project Structure

```
PillMate/
├── backend/
│   ├── server.py              # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables (not committed)
│
├── frontend/
│   ├── src/
│   │   ├── App.js             # Main React component & routing
│   │   ├── pages/             # Page components
│   │   │   ├── HomePage.js
│   │   │   ├── UploadPage.js
│   │   │   └── MedicationsPage.js
│   │   ├── components/ui/     # Shadcn/UI components
│   │   ├── hooks/             # Custom React hooks
│   │   └── lib/               # Utility functions
│   ├── public/                # Static assets
│   ├── package.json           # Node dependencies
│   ├── craco.config.js        # CRACO build configuration
│   ├── tailwind.config.js     # Tailwind CSS configuration
│   └── .env                   # Frontend environment variables
│
├── docs/                      # Documentation (you are here)
│   ├── README.md
│   ├── ARCHITECTURE.md
│   ├── FEATURES.md
│   ├── ALGORITHMS.md
│   └── MULTILANGUAGE_FEATURES.md (root)
│
├── design_guidelines.json     # UI/UX design specifications
├── QUICKSTART.md              # Quick start guide
├── LOCAL_SETUP.md             # Detailed local setup guide
├── MULTILANGUAGE_FEATURES.md  # Multi-language feature documentation
└── README.md                  # Project overview
```

---

## Key Technologies

### Backend
| Technology | Purpose |
|---|---|
| FastAPI | Modern Python web framework |
| MongoDB | NoSQL document database |
| Motor 3.6.0 | Async MongoDB driver |
| Pydantic | Data validation and serialization |
| Google Generative AI SDK | Gemini API integration |
| Uvicorn | ASGI server |

### Frontend
| Technology | Purpose |
|---|---|
| React 19 | UI library |
| React Router v7 | Client-side routing |
| CRACO | Custom build configuration |
| Tailwind CSS | Utility-first styling |
| Shadcn/UI | Accessible component library |
| Axios | HTTP client |
| Sonner | Toast notifications |

### AI / ML
| Technology | Purpose |
|---|---|
| Gemini 3 Flash Preview | Fast multimodal AI (vision + text) |
| Multi-language OCR | Prescription reading in any language |

---

## Key Features Summary

- **Multi-Language Prescription Reading** — Reads prescriptions in any language with automatic detection (98%+ accuracy)
- **Plain Language Explanations** — Converts medical jargon to simple language in 10+ languages
- **Behavioral Science (Nudge Theory)** — Explains "why timing matters" to increase adherence by 15–30%
- **Safety Features** — Contraindication checking, dosage safety reminders, visual warning system
- **Dosage Error Prevention** — Clear translations with preserved dosage amounts and safety warnings

---

## Testing

### Backend Tests
```bash
cd backend
python -m pytest ../tests/
```

### Manual API Testing
```bash
curl http://localhost:8001/api/
# Expected: {"message": "PillMate API - Multi-Language Prescription System"}

curl -X POST http://localhost:8001/api/prescriptions/upload \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "...", "preferred_language": "en"}'
```

---

## Security Considerations

### Data Protection
- **Image Data**: Only the first 100 characters stored
- **Patient Privacy**: Minimal PII storage
- **Encryption**: HTTPS for all communications
- **API Keys**: Environment variables only — never committed to version control

### Medical Safety
- **Disclaimers**: All AI checks include a medical-advice disclaimer
- **Validation**: Pydantic models for all inputs
- **Error Handling**: Graceful degradation with safe defaults

---

## Performance Metrics

| Metric | Value |
|---|---|
| Prescription Analysis | 5–8 seconds |
| Medication Explanation | 2–3 seconds |
| Contraindication Check | 2–3 seconds |
| Language Detection Accuracy | 98%+ |
| OCR Success Rate (clear images) | 95%+ |

---

## Troubleshooting

### Backend not starting
- Verify Python virtual environment is activated
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Ensure MongoDB is running: `mongosh`
- Confirm `GEMINI_API_KEY` is set in `backend/.env`

### Frontend not loading
- Run `npm install` to ensure dependencies are up to date
- Check that `REACT_APP_BACKEND_URL=http://localhost:8001` is set in `frontend/.env`
- Verify backend is running on port 8001

### AI API errors
- Verify `GEMINI_API_KEY` is valid
- Check API key quota / rate limits
- Review backend terminal logs for details

### Database connection issues
- Verify `MONGO_URL` is correct in `backend/.env`
- Check MongoDB is running: `mongosh`

---

## Contributing

### Documentation Guidelines
1. Keep language clear and concise
2. Include code examples where helpful
3. Add diagrams for complex flows
4. Update the table of contents
5. Follow existing formatting conventions

### Code Documentation
- Docstrings for all functions
- Inline comments for complex logic
- Type hints for all parameters

---

**PillMate** — Prescription Adherence Management System
