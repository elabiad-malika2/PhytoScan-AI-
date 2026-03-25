from sqlalchemy.orm import Session
from app.models.query import Query

def save_chat_history(db: Session, user_id: int, question: str, response: str):
    """Sauvegarde la conversation dans l'historique de l'utilisateur."""
    new_query = Query(
        user_id=user_id,
        query=question,
        response=response
    )
    db.add(new_query)
    db.commit()
    db.refresh(new_query)
    return new_query

def get_user_chat_history(db: Session, user_id: int):
    """Récupère tout l'historique d'un utilisateur (pour le Dashboard Front-end)."""
    return db.query(Query).filter(Query.user_id == user_id).order_by(Query.id.desc()).all()