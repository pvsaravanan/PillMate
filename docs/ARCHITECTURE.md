# PillMate — System Architecture Documentation

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Core Components](#core-components)
5. [Data Flow](#data-flow)
6. [AI Integration](#ai-integration)
7. [Security & Privacy](#security--privacy)

---

## Overview

PillMate is a multi-language prescription adherence management system that uses AI to:
- Extract medication information from prescription images in any language
- Translate complex medical information into plain language
- Prevent dosage errors through clear communication
- Increase medication adherence using behavioral science (Nudge Theory)

### Problem Solved
Complex prescriptions in multiple languages often lead to dosage errors.

### Solution
- Multi-language OCR for prescription reading
- AI-powered translation and explanation
- Behavioral nudges to explain why timing matters
- Safety checks for contraindications

---

## System Architecture

### High-Level Architecture

```
┌─────────────┐
│   React 19  │  ← Frontend (User Interface)
│  Frontend   │
└──────┬──────┘
       │
       │ HTTP / REST API
       │
┌──────▼──────┐
│   FastAPI   │  ← Backend (Business Logic)
│   Backend   │
└──────┬──────┘
       │
       ├─────────────────┬─────────────────┐
       │                 │                 │
┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
│   MongoDB   │  │   Google    │  │  Gemini AI  │
│  Database   │  │  Gemini API │  │   Vision    │
└─────────────┘  └─────────────┘  └─────────────┘
```

### Component Diagram

```
┌────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                       │
├────────────────────────────────────────────────────────┤
│  React 19 · React Router v7 · CRACO Build Tool         │
│  Tailwind CSS · Shadcn/UI · Axios · Sonner             │
│                                                        │
│  Pages:                                                │
│  ├── HomePage (Landing)                                │
│  ├── UploadPage (Prescription Upload)                  │
│  └── MedicationsPage (Medication Management)           │
└────────────────────────────────────────────────────────┘
                        ▼
┌────────────────────────────────────────────────────────┐
│                     API LAYER                          │
├────────────────────────────────────────────────────────┤
│  REST API Endpoints:                                   │
│  - POST /api/prescriptions/upload                      │
│  - GET  /api/prescriptions                             │
│  - POST /api/medications                               │
│  - GET  /api/medications                               │
│  - POST /api/contraindications/check                   │
│  - GET  /api/languages                                 │
└────────────────────────────────────────────────────────┘
                        ▼
┌────────────────────────────────────────────────────────┐
│                  BUSINESS LOGIC LAYER                   │
├────────────────────────────────────────────────────────┤
│  Core Services:                                        │
│  ├── Prescription Analysis Service                     │
│  ├── Language Detection Service                        │
│  ├── Translation Service                               │
│  ├── Medication Explanation Generator                  │
│  ├── Contraindication Checker                          │
│  └── Nudge Theory Engine                               │
└────────────────────────────────────────────────────────┘
                        ▼
┌─────────────────┬──────────────────┬──────────────────┐
│  DATA LAYER     │   AI LAYER       │  CACHE LAYER     │
├─────────────────┼──────────────────┼──────────────────┤
│  MongoDB        │  Google Gemini   │  In-Memory       │
│  Collections:   │  Model:          │  Cache           │
│  - prescriptions│  - gemini-3-     │  - Language Map  │
│  - medications  │    flash-preview │  - Model Config  │
└─────────────────┴──────────────────┴──────────────────┘
```

---

## Technology Stack

### Frontend
| Technology | Purpose |
|---|---|
| **React 19** | UI library |
| **React Router v7** | Client-side routing |
| **CRACO** | Custom build configuration (extends CRA) |
| **Tailwind CSS** | Utility-first styling |
| **Shadcn/UI** | Accessible component library (Radix primitives) |
| **Axios** | HTTP client for API calls |
| **Sonner** | Toast notifications |

### Backend
| Technology | Purpose |
|---|---|
| **FastAPI** | Modern Python web framework |
| **Python 3.11+** | Programming language |
| **Pydantic** | Data validation and serialization |
| **Motor 3.6.0** | Async MongoDB driver |
| **python-dotenv** | Environment variable management |
| **Uvicorn** | ASGI server |

### AI & ML
| Technology | Purpose |
|---|---|
| **Google Generative AI SDK** (`google-generativeai`) | Gemini integration |
| **Gemini 3 Flash Preview** | Fast multimodal model for vision + text |

### Database
| Technology | Purpose |
|---|---|
| **MongoDB** | NoSQL document database |
| **Motor 3.6.0** | Async Python driver |

---

## Core Components

### 1. Prescription Upload & Analysis

**Function**: `analyze_prescription_image()`

**Purpose**: Extract medication information from prescription images in any language.

**Input**:
- Base64-encoded image
- Preferred output language

**Process**:
1. Initialize Gemini Vision model
2. Send image with multi-language OCR prompt
3. Detect prescription language
4. Extract medication details (name, dosage, frequency, timing, special instructions)

**Output**:
```json
{
  "detected_language": "es",
  "extracted_text": "Full OCR text",
  "medications": [
    {
      "name": "Metformina",
      "name_english": "Metformin",
      "dosage": "500mg",
      "frequency": "Dos veces al día",
      "timing": ["mañana", "noche"],
      "with_food": true
    }
  ]
}
```

### 2. Plain Language Explanation Generator

**Function**: `generate_medication_explanation()`

**Purpose**: Create simple, understandable medication explanations using Nudge Theory.

**Nudge Theory Implementation**:
- **Motivation**: Explain consequences of poor timing
- **Meaning**: Connect actions to health outcomes
- **Simplicity**: Remove medical jargon
- **Positive Framing**: Focus on benefits, not penalties

### 3. Multi-Language Translation System

**Supported Languages**: 10+ languages including English, Spanish, Hindi, Arabic, Chinese, French, German, Portuguese, Russian, and Japanese.

**Translation Flow**:
```
Prescription (Any Language)
        ↓
    Detection
        ↓
    Extraction
        ↓
 User Language Preference
        ↓
   AI Translation
        ↓
Plain Language Explanation
```

### 4. Contraindication Checker

**Function**: `check_drug_interactions()`

**Purpose**: Identify potential drug interactions across a patient's medication list.

**Safety Note**: Intended for basic checking only. Users are always advised to consult their healthcare provider.

### 5. Data Persistence Layer

**Database**: MongoDB (document-based)

**Collections**:

**prescriptions**:
```json
{
  "id": "uuid",
  "patient_id": "string",
  "image_data": "truncated_base64",
  "extracted_text": "string",
  "detected_language": "es",
  "preferred_language": "en",
  "medications": [],
  "analysis_complete": true,
  "created_at": "ISO8601"
}
```

**medications**:
```json
{
  "id": "uuid",
  "name": "Metformin",
  "dosage": "500mg",
  "frequency": "Twice daily",
  "timing": ["morning", "evening"],
  "plain_language_explanation": "string",
  "why_timing_matters": "string",
  "warnings": ["string"],
  "original_language": "es",
  "translated_to": "en",
  "created_at": "ISO8601"
}
```

---

## Data Flow

### Prescription Upload Flow

```
┌─────────┐
│  User   │
└────┬────┘
     │ 1. Select prescription image
     ▼
┌─────────────┐
│  Frontend   │
│  (Upload)   │
└─────┬───────┘
      │ 2. Convert to Base64
      │ 3. POST /api/prescriptions/upload
      ▼
┌──────────────┐
│   Backend    │
│   FastAPI    │
└─────┬────────┘
      │ 4. Validate input
      │ 5. Call Gemini Vision API
      ▼
┌──────────────┐
│ Gemini Vision│
│     API      │
└─────┬────────┘
      │ 6. OCR + Language Detection
      │ 7. Return JSON
      ▼
┌──────────────┐
│   Backend    │
│  (Process)   │
└─────┬────────┘
      │ 8. For each medication:
      │    - Generate explanation
      │    - Apply Nudge Theory
      │    - Add safety warnings
      ▼
┌──────────────┐
│   MongoDB    │
│   (Store)    │
└─────┬────────┘
      │ 9. Return prescription object
      ▼
┌──────────────┐
│  Frontend    │
│  (Display)   │
└──────────────┘
```

---

## AI Integration

### Google Gemini Configuration

**Model**: `gemini-3-flash-preview`

**Why Gemini 3 Flash?**
- Fast response times (< 2 seconds)
- Cost-effective for production use
- Supports vision + text (multimodal)
- High accuracy for medical text extraction
- Strong multi-language capabilities

**Configuration**:
```python
genai.GenerativeModel(
    model_name='gemini-3-flash-preview',
    generation_config={
        "temperature": 0.3,
        "top_p": 0.95,
        "max_output_tokens": 2048
    }
)
```

### Prompt Engineering

**Prescription Analysis Prompt**:
- Multi-language instruction
- JSON schema specification
- Error handling guidance

**Explanation Prompt**:
- Target language specification
- Plain language requirement
- Nudge Theory framework
- Safety reminder inclusion

### Response Parsing

**Function**: `extract_json_from_response()`

Strips markdown fencing, locates JSON boundaries, and parses with `json.loads()`, falling back to safe defaults on error.

---

## Security & Privacy

### Data Protection
- **Image Data**: Only the first 100 characters are stored (reference only)
- **Patient Privacy**: No PII stored beyond `patient_id`
- **Encryption**: HTTPS for all API calls
- **API Keys**: Environment variables only — never committed to source control

### Medical Content Safety
- **Disclaimers**: All contraindication checks include a medical-advice disclaimer
- **Validation**: All inputs validated with Pydantic models
- **Error Handling**: Graceful degradation with safe defaults

---

## Performance Considerations

### Response Times
| Operation | Typical Duration |
|---|---|
| Prescription Analysis | 5–8 s |
| Medication Explanation | 2–3 s |
| Contraindication Check | 2–3 s |

### Optimization Strategies
- Async/await for all I/O operations
- MongoDB indexing on `patient_id`
- Image compression before upload
- Non-blocking request handling via Uvicorn

---

## Future Enhancements

1. **Real-time Reminders** — SMS / Push notifications
2. **Voice Support** — Audio explanations in multiple languages
3. **Prescription History** — Trend analysis
4. **Family Sharing** — Multi-user support
5. **Pharmacy Integration** — Direct prescription filling
6. **ML Optimization** — Fine-tuned models for medical text
