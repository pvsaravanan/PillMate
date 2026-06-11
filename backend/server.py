from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

from database import lifespan
from models import LanguageList
from services.ai_service import SUPPORTED_LANGUAGES
from routes.prescriptions import router as prescriptions_router
from routes.medications import router as medications_router
from routes.contraindications import router as contraindications_router
from routes.adherence import router as adherence_router

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

app = FastAPI(title="PillGuide API", version="2.0", lifespan=lifespan)
api_router = APIRouter(prefix="/api")

@api_router.get("/")
async def root():
    return {"message": "PillGuide API - Multi-Language Prescription System"}

@api_router.get("/languages", response_model=LanguageList)
async def get_supported_languages():
    return {"languages": SUPPORTED_LANGUAGES}

# Include child routers
api_router.include_router(prescriptions_router)
api_router.include_router(medications_router)
api_router.include_router(contraindications_router)
api_router.include_router(adherence_router)

# Mount API router
app.include_router(api_router)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)