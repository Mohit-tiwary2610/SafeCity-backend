from fastapi import APIRouter
from pydantic import BaseModel, Field
from datetime import datetime
from ..core.db import db
from ..utils.geofuzz import fuzz
from ..services.nlp import predict
from enum import Enum

router = APIRouter()

# Define severity levels as an Enum for validation + Swagger dropdown
class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class IncidentIn(BaseModel):
    type: str | None = Field(None, pattern="^(harassment|theft|unsafe_area|hazard|emergency)$")
    severity: Severity   # ✅ changed from int to string Enum
    description: str = Field(..., max_length=800)
    lat: float
    lng: float
    consent_public_map: bool = False
    media_urls: list[str] = []

# ✅ GET route for frontend dashboard
@router.get("/")
async def get_all_incidents():
    try:
        cursor = db.incidents.find().sort("created_at", -1)
        incidents = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
            incidents.append(doc)
        return {"ok": True, "incidents": incidents}
    except Exception as e:
        print("❌ Error in get_all_incidents:", e)
        return {"ok": False, "error": str(e)}

@router.post("/")
async def create_incident(incident: IncidentIn):
    try:
        inf_type = incident.type or predict(incident.description)
        f_lat, f_lng = fuzz(incident.lat, incident.lng)
        doc = {
            "type": inf_type,
            "severity": incident.severity,  # Enum will be stored as string
            "description": incident.description,
            "lat": incident.lat, "lng": incident.lng,
            "f_lat": f_lat, "f_lng": f_lng,
            "consent_public_map": incident.consent_public_map,
            "media_urls": incident.media_urls,
            "status": "pending",
            "created_at": datetime.utcnow(),
        }
        res = await db.incidents.insert_one(doc)
        return {"ok": True, "id": str(res.inserted_id), "type": inf_type}
    except Exception as e:
        print("❌ Error in create_incident:", e)
        return {"ok": False, "error": str(e)}