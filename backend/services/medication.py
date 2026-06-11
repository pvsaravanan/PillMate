from typing import List, Optional
from datetime import datetime
import json
from fastapi import HTTPException
import logging

from database import db
from models import Medication, MedicationCreate, Prescription, PrescriptionCreate
from services.ai_service import (
    analyze_prescription_image,
    generate_medication_explanation
)

async def add_medication_manually(data: MedicationCreate) -> Medication:
    explanation_data = await generate_medication_explanation(
        data.name,
        data.dosage,
        data.frequency,
        data.preferred_language
    )
    
    full_explanation = f"{explanation_data['plain_explanation']} ⚠️ {explanation_data.get('dosage_safety_reminder', '')}"
    
    medication = Medication(
        name=data.name,
        dosage=data.dosage,
        frequency=data.frequency,
        timing=data.timing,
        duration=data.duration,
        with_food=data.with_food,
        plain_language_explanation=full_explanation,
        why_timing_matters=explanation_data['why_timing_matters'],
        warnings=[explanation_data.get('dosage_safety_reminder', '')],
        translated_to=data.preferred_language
    )
    
    doc = medication.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.medications.insert_one(doc)
    return medication

async def get_medications(skip: int = 0, limit: int = 100) -> List[dict]:
    medications = await db.medications.find({}, {"_id": 0}).skip(skip).limit(limit).to_list(limit)
    
    for med in medications:
        if isinstance(med['created_at'], str):
            med['created_at'] = datetime.fromisoformat(med['created_at'])
            
    return medications

async def upload_prescription(data: PrescriptionCreate) -> Prescription:
    try:
        extraction_result = await analyze_prescription_image(
            data.image_base64, 
            data.preferred_language
        )
        
        detected_lang = extraction_result['detected_language']
        
        medications_with_explanation = []
        for med in extraction_result.get("medications", []):
            if not med.get('name'):
                continue
            
            med_name = med.get('name_english', med.get('name', 'Unknown'))
            
            explanation_data = await generate_medication_explanation(
                med_name,
                med.get('dosage', 'Unknown'),
                med.get('frequency', 'as prescribed'),
                data.preferred_language
            )
            
            full_explanation = f"{explanation_data['plain_explanation']} ⚠️ {explanation_data.get('dosage_safety_reminder', '')}"
            
            medication_obj = Medication(
                name=med_name,
                dosage=med.get('dosage', 'As prescribed'),
                frequency=med.get('frequency', 'As prescribed'),
                timing=med.get('timing', []),
                duration=med.get('duration'),
                with_food=med.get('with_food', False),
                plain_language_explanation=full_explanation,
                why_timing_matters=explanation_data['why_timing_matters'],
                warnings=[explanation_data.get('dosage_safety_reminder', '')],
                original_language=detected_lang,
                translated_to=data.preferred_language
            )
            medications_with_explanation.append(medication_obj)
        
        prescription = Prescription(
            patient_id=data.patient_id,
            image_data=data.image_base64[:100],
            extracted_text=extraction_result.get("extracted_text", ""),
            detected_language=detected_lang,
            preferred_language=data.preferred_language,
            medications=medications_with_explanation,
            analysis_complete=True
        )
        
        doc = prescription.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        for med in doc['medications']:
            med['created_at'] = med['created_at'].isoformat()
        
        await db.prescriptions.insert_one(doc)
        return prescription
        
    except json.JSONDecodeError as e:
        logging.error(f"JSON parsing error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Failed to parse AI response. The prescription image may be unclear."
        )
    except Exception as e:
        logging.error(f"Error analyzing prescription: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze prescription: {str(e)}")

async def get_prescriptions(patient_id: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[dict]:
    query = {"patient_id": patient_id} if patient_id else {}
    prescriptions = await db.prescriptions.find(query, {"_id": 0}).skip(skip).limit(limit).to_list(limit)
    
    for prescription in prescriptions:
        if isinstance(prescription['created_at'], str):
            prescription['created_at'] = datetime.fromisoformat(prescription['created_at'])
        for med in prescription.get('medications', []):
            if isinstance(med['created_at'], str):
                med['created_at'] = datetime.fromisoformat(med['created_at'])
                
    return prescriptions
