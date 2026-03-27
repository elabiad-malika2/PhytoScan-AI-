from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_user,get_current_agriculteur
from app.models.user import User

# Imports de l'Étape 3 (Pydantic)
from app.schemas.chat_schema import ChatRequest, ChatResponse, ChatHistoryResponse
# Imports de l'Étape 2 (DAL)
from app.dal.query_dal import save_chat_history, get_user_chat_history
# Import de l'IA RAG
from app.services.rag.generator import generate_agricultural_advice

router = APIRouter()

@router.post("/ask", response_model=ChatResponse)
def poser_question_expert(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_agriculteur) 
):
    try:
        rag_result = generate_agricultural_advice(
            maladie_detectee=request.question,
            langue=request.langue
        )
        
        save_chat_history(
            db=db,
            user_id=current_user.id,
            question=request.question,
            response=rag_result["rapport_ia"]
        )

        return {
            "question_posee": request.question,
            "rapport_ia": rag_result["rapport_ia"],
            "ressource_officielle": rag_result.get("ressource_officielle")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de l'IA : {str(e)}")



@router.get("/history", response_model=List[ChatHistoryResponse])
def obtenir_historique_chat(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_agriculteur)
):
    """Renvoie toutes les anciennes questions/réponses de l'agriculteur."""
    
    historique = get_user_chat_history(db, current_user.id)
    return historique