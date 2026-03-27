from pydantic import BaseModel
from datetime import datetime


class ScanAnalyzeResponse(BaseModel):
    status: str
    scan_id: int
    maladie_detectee: str
    rapport_expert: str
    source: str
    image_url: str


class ScanHistoryResponse(BaseModel):
    id: int
    image_path: str
    disease_detected: str
    created_at: datetime

    class Config:
        from_attributes = True 