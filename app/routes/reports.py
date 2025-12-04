from fastapi import APIRouter
from app.core.db import db
from bson import ObjectId

router = APIRouter()

def serialize_report(report):
    return {
        "_id": str(report.get("_id")),
        "type": report.get("type"),
        "description": report.get("description"),
        "severity": report.get("severity"),
        "status": report.get("status"),
        "f_lat": report.get("f_lat"),
        "f_lng": report.get("f_lng"),
    }

@router.get("/")
async def get_reports():
    try:
        raw_reports = [r async for r in db.incidents.find()]
        return [serialize_report(r) for r in raw_reports]
    except Exception as e:
        return {"error": str(e)}