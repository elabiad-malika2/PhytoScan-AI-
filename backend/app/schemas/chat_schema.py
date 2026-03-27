from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatRequest(BaseModel):
    question: str
    langue: str = "fr"

class ChatResponse(BaseModel):
    question_posee: str
    rapport_ia: str
    ressource_officielle: Optional[str] = None

class ChatHistoryResponse(BaseModel):
    id: int
    query: str
    response: str
    created_at: datetime

    class Config:
        from_attributes = True