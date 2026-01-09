from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import os

router = APIRouter()

class SignupBody(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(body: SignupBody):
    try:
        client = MongoClient(os.getenv("MONGO_URI"))
        db = client[os.getenv("DB_NAME", "safecity")]
        users = db["users"]

        # Check if user exists
        if users.find_one({"email": body.email}):
            raise HTTPException(status_code=400, detail="Email already registered")

        users.insert_one({"email": body.email, "password": body.password})
        return {"ok": True, "message": "User created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")