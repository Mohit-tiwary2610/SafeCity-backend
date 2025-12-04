from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class UploadInit(BaseModel):
    filename: str

@router.post("/init")
def init_upload(_: UploadInit):
    return {"upload_preset": "safecity_blur", "folder": "safecity"}