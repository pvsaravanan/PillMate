from fastapi import APIRouter, HTTPException
from typing import List
from models import Medication, MedicationCreate
from services import medication as medication_service

router = APIRouter(prefix="/medications")

@router.post("", response_model=Medication)
async def add_medication_manually(data: MedicationCreate):
    try:
        return await medication_service.add_medication_manually(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[Medication])
async def get_medications(skip: int = 0, limit: int = 100):
    try:
        return await medication_service.get_medications(skip, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
