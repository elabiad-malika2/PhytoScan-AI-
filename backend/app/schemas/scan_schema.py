# Schéma Scan (Pydantic)
from pydantic import BaseModel
from datetime import datetime

# -----------------------------------------------------------------
# RÉPONSE LORS D'UNE ANALYSE (POST /api/v1/scans/analyze)
# -----------------------------------------------------------------
class ScanAnalyzeResponse(BaseModel):
    status: str
    scan_id: int
    maladie_detectee: str
    rapport_expert: str
    source: str
    image_url: str

# -----------------------------------------------------------------
# RÉPONSE LORS DE LA CONSULTATION DE L'HISTORIQUE (GET /api/v1/reports/history)
# -----------------------------------------------------------------
class ScanHistoryResponse(BaseModel):
    id: int
    image_path: str
    disease_detected: str
    created_at: datetime

    class Config:
        from_attributes = True # Autorise Pydantic à lire les objets SQLAlchemy !