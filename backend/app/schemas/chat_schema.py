from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 1. Ce que React envoie à FastAPI (POST /ask)
class ChatRequest(BaseModel):
    question: str
    langue: str = "fr"

# 2. Ce que FastAPI répond à React (POST /ask)
class ChatResponse(BaseModel):
    question_posee: str
    rapport_ia: str
    ressource_officielle: Optional[str] = None

# 3. Ce que FastAPI renvoie quand on demande l'historique (GET /history)
class ChatHistoryResponse(BaseModel):
    id: int
    query: str
    response: str
    created_at: datetime

    class Config:
        from_attributes = True # Autorise la lecture depuis SQLAlchemy