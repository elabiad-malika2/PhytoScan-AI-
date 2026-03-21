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

# ==========================================
# ROUTE 1 : POSER UNE QUESTION AU CHATBOT
# ==========================================
@router.post("/ask", response_model=ChatResponse)
def poser_question_expert(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_agriculteur) # Vérifie que l'agriculteur est connecté
):
    try:
        # 1. On donne la question au RAG (Gemini + ChromaDB)
        rag_result = generate_agricultural_advice(
            maladie_detectee=request.question,
            langue=request.langue
        )
        
        # 2. On sauvegarde la discussion dans la table `queries` via le DAL
        save_chat_history(
            db=db,
            user_id=current_user.id,
            question=request.question,
            response=rag_result["rapport_ia"]
        )

        # 3. On renvoie la réponse au Frontend
        return {
            "question_posee": request.question,
            "rapport_ia": rag_result["rapport_ia"],
            "ressource_officielle": rag_result.get("ressource_officielle")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de l'IA : {str(e)}")


# ==========================================
# ROUTE 2 : VOIR SON HISTORIQUE DE CHAT
# ==========================================
@router.get("/history", response_model=List[ChatHistoryResponse])
def obtenir_historique_chat(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_agriculteur)
):
    """Renvoie toutes les anciennes questions/réponses de l'agriculteur."""
    
    # Appelle le DAL pour lire la table `queries`
    historique = get_user_chat_history(db, current_user.id)
    return historique