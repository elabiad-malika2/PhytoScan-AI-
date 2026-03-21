# Schéma Report (Pydantic)
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReportResponse(BaseModel):
    id: int
    scan_id: int
    treatment_recommendation: str
    pdf_path: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True