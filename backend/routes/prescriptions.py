from fastapi import APIRouter, HTTPException
from typing import List, Optional
from models import Prescription, PrescriptionCreate
from services import medication as medication_service

router = APIRouter(prefix="/prescriptions")

@router.post("/upload", response_model=Prescription)
async def upload_prescription(data: PrescriptionCreate):
    # 5MB size limit represented in base64 (~7,000,000 characters)
    if len(data.image_base64) > 7_000_000:
        raise HTTPException(
            status_code=400,
            detail="Prescription image is too large. Max size allowed is 5MB."
        )
    try:
        return await medication_service.upload_prescription(data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[Prescription])
async def get_prescriptions(patient_id: Optional[str] = None, skip: int = 0, limit: int = 100):
    try:
        return await medication_service.get_prescriptions(patient_id, skip, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
