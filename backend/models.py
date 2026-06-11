from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone

class PrescriptionCreate(BaseModel):
    image_base64: str
    patient_id: Optional[str] = None
    preferred_language: str = "en"

class Medication(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    dosage: str
    frequency: str
    timing: List[str]
    duration: Optional[str] = None
    plain_language_explanation: str
    why_timing_matters: str
    with_food: Optional[bool] = False
    warnings: List[str] = []
    original_language: Optional[str] = None
    translated_to: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Prescription(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: Optional[str] = None
    image_data: str
    extracted_text: str
    detected_language: str
    preferred_language: str
    medications: List[Medication]
    analysis_complete: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MedicationCreate(BaseModel):
    name: str
    dosage: str
    frequency: str
    timing: List[str]
    duration: Optional[str] = None
    with_food: bool = False
    preferred_language: str = "en"

class ContraindictionCheck(BaseModel):
    medication_name: str
    current_medications: List[str]
    preferred_language: str = "en"

class ContraindictionResult(BaseModel):
    has_contraindications: bool
    warnings: List[str]
    recommendations: str

class LanguageList(BaseModel):
    languages: dict

class AdherenceLog(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    medication_id: str
    medication_name: str
    date: str  # YYYY-MM-DD
    time_slot: str  # e.g., morning, evening
    status: str  # taken, skipped
    logged_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AdherenceLogCreate(BaseModel):
    medication_id: str
    medication_name: str
    date: str
    time_slot: str
    status: str
