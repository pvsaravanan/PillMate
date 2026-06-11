from datetime import datetime, timezone
import uuid
from typing import List
from database import db
from models import AdherenceLog, AdherenceLogCreate

async def log_adherence(data: AdherenceLogCreate) -> AdherenceLog:
    existing = await db.adherence_logs.find_one({
        "medication_id": data.medication_id,
        "date": data.date,
        "time_slot": data.time_slot
    })
    
    if existing:
        await db.adherence_logs.update_one(
            {"_id": existing["_id"]},
            {"$set": {"status": data.status, "logged_at": datetime.now(timezone.utc).isoformat()}}
        )
        updated = await db.adherence_logs.find_one({"_id": existing["_id"]})
        return AdherenceLog(
            id=updated.get("id", str(uuid.uuid4())),
            medication_id=updated["medication_id"],
            medication_name=updated["medication_name"],
            date=updated["date"],
            time_slot=updated["time_slot"],
            status=updated["status"],
            logged_at=datetime.fromisoformat(updated["logged_at"]) if isinstance(updated["logged_at"], str) else updated["logged_at"]
        )
    else:
        log_obj = AdherenceLog(
            medication_id=data.medication_id,
            medication_name=data.medication_name,
            date=data.date,
            time_slot=data.time_slot,
            status=data.status
        )
        doc = log_obj.model_dump()
        doc['logged_at'] = doc['logged_at'].isoformat()
        await db.adherence_logs.insert_one(doc)
        return log_obj

async def get_adherence(start_date: str, end_date: str) -> List[dict]:
    logs = await db.adherence_logs.find({
        "date": {"$gte": start_date, "$lte": end_date}
    }, {"_id": 0}).to_list(10000)
    
    for log in logs:
        if isinstance(log['logged_at'], str):
            log['logged_at'] = datetime.fromisoformat(log['logged_at'])
    return logs

async def get_adherence_stats(start_date: str, end_date: str) -> dict:
    logs = await db.adherence_logs.find({
        "date": {"$gte": start_date, "$lte": end_date}
    }).to_list(10000)
    
    taken = sum(1 for log in logs if log.get("status") == "taken")
    skipped = sum(1 for log in logs if log.get("status") == "skipped")
    total = taken + skipped
    
    adherence_rate = (taken / total * 100) if total > 0 else 100.0
    
    return {
        "taken": taken,
        "skipped": skipped,
        "total": total,
        "adherence_rate": round(adherence_rate, 2)
    }
