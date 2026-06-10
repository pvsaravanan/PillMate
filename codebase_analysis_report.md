# PillMate Codebase Analysis Report

This report provides a comprehensive analysis of the **PillMate** codebase, a multi-language prescription analysis and medication management platform. PillMate leverages modern web technologies (React and FastAPI) combined with Google Gemini AI to assist users in understanding their prescriptions, identifying potential drug interactions, and maintaining high medication adherence using behavioral science.

---

## 1. Directory Structure

The repository follows a clean fullstack separation, split into a frontend UI layer and a backend service layer.

```
PillMate/
├── backend/
│   ├── server.py              # FastAPI Application and endpoints
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables (local config)
├── frontend/
│   ├── public/                # Public assets and index.html
│   ├── src/
│   │   ├── App.js             # Client routing and shell
│   │   ├── App.css            # Custom layout rules
│   │   ├── index.js           # DOM entrypoint
│   │   ├── index.css          # Tailwind imports & CSS theme variables
│   │   ├── components/ui/     # Reusable shadcn/ui components
│   │   ├── pages/             # Page components (HomePage, UploadPage, MedicationsPage)
│   │   └── lib/               # Shared libraries (utils.js)
│   ├── package.json           # Node.js dependencies
│   ├── craco.config.js        # Craco Webpack extension
│   └── tailwind.config.js     # Tailwind design system configuration
├── docs/                      # Architectural & feature specifications
│   ├── ARCHITECTURE.md
│   ├── ALGORITHMS.md
│   ├── FEATURES.md
│   └── README.md
├── design_guidelines.json     # Curated design tokens, typography, and constraints
├── QUICKSTART.md              # Setup guide
├── LOCAL_SETUP.md             # Developer local setup details
└── README.md                  # Root overview documentation
```

---

## 2. Technical Stack & Component Analysis

### Backend Layer (`/backend`)
*   **Web Framework:** FastAPI (v0.110.1) served with Uvicorn (v0.25.0).
*   **Database Client:** `motor` (v3.6.0) providing an asynchronous interface for MongoDB.
*   **AI SDK:** `google-generativeai` (v0.8.6) targeting the `gemini-3-flash-preview` model.
*   **Data Validation:** Pydantic (v2.12.5) for schema definition, type checking, and coercion.

#### Key APIs & Services:
1.  **`POST /api/prescriptions/upload`**: Takes a Base64 encoded image and language preference. Performs OCR and analysis using Gemini Vision, generates custom explanations, structures medications, and inserts a prescription record into MongoDB.
2.  **`GET /api/prescriptions`**: Fetches past uploads filtered by `patient_id`.
3.  **`POST /api/medications`**: Allows manual registration of medication. Automatically triggers Gemini to generate plain-language advice and timing logic.
4.  **`POST /api/contraindications/check`**: Checks for potential drug-drug interactions between a new candidate drug and a list of existing active medications.
5.  **`GET /api/languages`**: Lists supported languages dynamically.

### Frontend Layer (`/frontend`)
*   **Core Engine:** React 19 and React Router DOM v7.
*   **Styling:** Tailwind CSS (v3.4.17) with custom HSL palette variables based on Radix UI primitives.
*   **Build Tooling:** Craco (v7.1.0) extending Create React App configurations.
*   **Interactive Components:** Form management via `react-hook-form` paired with `zod` for validation, plus chart visualization using `recharts` (v3.6.0).

---

## 3. Design System & User Interface (UI)

PillMate uses a curated, warm design system called **"E1 - The Anti-AI Designer"** configured inside [design_guidelines.json](file:///c:/proj/PillMate/design_guidelines.json):
*   **Typography:** Expressive serif headings (`Fraunces`) combined with highly legible geometric sans-serif body copy (`Plus Jakarta Sans`).
*   **Color Palette:** Warm organic colors to establish empathy:
    *   **Primary (Sage Wisdom):** `#4A6C58` (representing calm, health, trust).
    *   **Secondary (Clay Earth):** `#C88D73` (representing warmth, attention, alerts).
    *   **Background (Paper White):** `#FDFCF8` (reducing eye strain compared to pure white).
*   **Layout Strategy:** Asymmetric bento grid layouts, pill-shaped buttons, and soft ambient shadows (no harsh black styles).

---

## 4. AI Processing & Behavioral Design

PillMate implements custom algorithms detailed in [ALGORITHMS.md](file:///c:/proj/PillMate/docs/ALGORITHMS.md):

```
       Image Upload (Base64)
                 │
                 ▼
     [Gemini Multimodal OCR]
  (Extracts meds & original text)
                 │
                 ▼
  [Explanation & Nudge Engine]
(Applies Nudge Theory / translations)
                 │
                 ▼
    [Contraindication Check]
  (Identifies critical warnings)
                 │
                 ▼
      Saved to MongoDB & UI
```

### Behavioral Science Integration (Nudge Theory)
The platform focuses on improving patient adherence. Instead of clinical jargon, the AI-generated responses construct a **"Why Timing Matters"** nudge using:
1.  **Habit Stacking:** Linking pill schedules to daily milestones (e.g. coffee, meals).
2.  **Positive Framing:** Connecting correct ingestion to immediate and long-term health improvements.
3.  **Simplicity:** Translating complex instructions (e.g., *BID with meals*) into plain actions (*one pill with breakfast and dinner*).

---

## 5. Security, Privacy & Medical Safety

*   **Minimization of PII:** PillMate does not store patient identity details other than an optional, anonymous `patient_id`.
*   **Prescription Image Protection:** Raw prescription images represent sensitive health information. To protect user privacy, the backend only persists the first 100 characters of the Base64 image payload as reference, discarding the full image immediately after the OCR phase.
*   **Medical Disclaimers:** Every interaction warning or explanation generated by AI appends a clear recommendation warning the user to consult a doctor or pharmacist.

---

## 6. Recommendations & Observations

While the codebase is clean, modular, and structurally sound, the following areas present opportunities for optimization:

1.  **Model version stabilization:** The backend utilizes the model `gemini-3-flash-preview`. In production environments, it is recommended to transition to stable aliases such as `gemini-2.5-flash` or newer general-availability (GA) endpoints to guarantee uptime and prompt behavior consistency.
2.  **State Management & Caching:** AI requests (image analysis and interaction checks) can take 3–8 seconds. Implementing Redis or MongoDB caching for common medication interaction lookups would significantly accelerate subsequent queries.
3.  **Database Indexing:** Ensure index constraints are declared on `patient_id` within the `prescriptions` collection, and on `name` or custom fields in the `medications` collection to maintain query speed as the database scales.
