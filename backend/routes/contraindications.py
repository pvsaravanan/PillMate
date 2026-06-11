from fastapi import APIRouter, HTTPException
from models import ContraindictionCheck, ContraindictionResult
from services import ai_service

router = APIRouter(prefix="/contraindications")

@router.post("/check", response_model=ContraindictionResult)
async def check_contraindications(data: ContraindictionCheck):
    try:
        result = await ai_service.check_drug_interactions(
            data.medication_name,
            data.current_medications,
            data.preferred_language
        )
        return ContraindictionResult(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
