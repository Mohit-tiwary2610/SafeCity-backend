from fastapi import APIRouter
from pydantic import BaseModel
from bson import ObjectId
from ..core.db import db

router = APIRouter()

class Review(BaseModel):
    id: str
    action: str  # "verify" or "reject"
    notes: str = ""

@router.post("/review")
async def review(r: Review):
    status = "verified" if r.action == "verify" else "rejected"
    await db.incidents.update_one({"_id": ObjectId(r.id)}, {"$set": {"status": status, "moderation_notes": r.notes}})
    return {"ok": True, "status": status}