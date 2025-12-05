from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import routers from the app/routes package
from app.routes import incidents, moderation, metrics, storage, reports

app = FastAPI(title="SafeCity")

# Enable CORS for frontend (localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"] for stricter security
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(incidents.router, prefix="/incidents", tags=["incidents"])
app.include_router(moderation.router, prefix="/moderation", tags=["moderation"])
app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
app.include_router(storage.router, prefix="/storage", tags=["storage"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])

# ✅ Root endpoint for quick check
@app.get("/")
def root():
    return {"message": "SafeCity backend is running"}

# ✅ Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}

# ✅ Prediction endpoint (placeholder for ML model)
class PredictionInput(BaseModel):
    text: str

@app.post("/predict")
def predict(input: PredictionInput):
    # Example placeholder logic — replace with your ML model inference
    result = "safe" if "police" in input.text.lower() else "unsafe"
    return {"prediction": result}