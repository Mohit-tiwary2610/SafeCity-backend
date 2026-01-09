# main.py
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pymongo import MongoClient

# Import routers from the app/routes package
from app.routes import incidents, moderation, metrics, storage, reports

app = FastAPI(title="SafeCity")

# ----- CORS -----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to your frontend origin in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Global error formatting (frontend sees a clean `detail` string) -----
@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": str(exc.detail)})

@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": str(exc)})

# ----- Mongo helpers -----
def _get_mongo_uri() -> str:
    uri = os.getenv("MONGO_URI")
    if not uri:
        raise HTTPException(status_code=500, detail="MONGO_URI missing in environment")
    return uri

def _get_db_name() -> str:
    return os.getenv("DB_NAME", "safecity")

def _mongo_client() -> MongoClient:
    # Small timeout so /health responds quickly on failure
    return MongoClient(_get_mongo_uri(), serverSelectionTimeoutMS=3000)

# ----- Routers -----
app.include_router(incidents.router, prefix="/incidents", tags=["incidents"])
app.include_router(moderation.router, prefix="/moderation", tags=["moderation"])
app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
app.include_router(storage.router, prefix="/storage", tags=["storage"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])

# ----- Root quick check -----
@app.get("/")
def root():
    return {"message": "SafeCity backend is running"}

# ----- Health check (tests MongoDB connection and lists collections) -----
@app.get("/health")
def health_check():
    try:
        client = _mongo_client()
        # Force connection attempt
        server_info = client.server_info()
        db_name = _get_db_name()
        db = client[db_name]
        collections = db.list_collection_names()
        return {
            "ok": True,
            "db": db_name,
            "collections": collections,
            "server": {
                "version": server_info.get("version"),
            },
        }
    except Exception as e:
        # Return a readable error for the frontend
        return JSONResponse(status_code=500, content={"ok": False, "detail": str(e)})

# ----- Prediction endpoint (placeholder for ML model) -----
class PredictionInput(BaseModel):
    text: str

@app.post("/predict")
def predict(input: PredictionInput):
    # Example placeholder logic — replace with your ML model inference
    result = "safe" if "police" in input.text.lower() else "unsafe"
    return {"prediction": result}