from fastapi import APIRouter, HTTPException
from typing import List
from models import AdherenceLog, AdherenceLogCreate
from services import adherence as adherence_service

router = APIRouter(prefix="/adherence")

@router.post("", response_model=AdherenceLog)
async def log_adherence(data: AdherenceLogCreate):
    try:
        return await adherence_service.log_adherence(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[AdherenceLog])
async def get_adherence(start_date: str, end_date: str):
    try:
        return await adherence_service.get_adherence(start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_adherence_stats(start_date: str, end_date: str):
    try:
        return await adherence_service.get_adherence_stats(start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
