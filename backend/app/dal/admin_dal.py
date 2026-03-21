from sqlalchemy.orm import Session
from app.models.user import User
from app.models.plant_scan import PlantScan
from app.models.query import Query

def get_all_agriculteurs(db: Session):
    """Récupère tous les agriculteurs inscrits."""
    return db.query(User).filter(User.role == "agriculteur").all()

def delete_user_by_id(db: Session, user_id: int):
    """Supprime un utilisateur (la BDD supprimera automatiquement ses scans et chats grâce au CASCADE)."""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

def get_platform_statistics(db: Session):
    """Récupère les statistiques globales pour le tableau de bord Admin."""
    total_users = db.query(User).filter(User.role == "agriculteur").count()
    total_scans = db.query(PlantScan).count()
    total_questions = db.query(Query).count()
    
    # Les 5 derniers scans sur la plateforme (pour que l'admin surveille)
    recent_scans = db.query(PlantScan).order_by(PlantScan.created_at.desc()).limit(5).all()

    return {
        "total_agriculteurs": total_users,
        "total_scans_realises": total_scans,
        "total_questions_posees": total_questions,
        "derniers_scans": [
            {"id": s.id, "maladie": s.disease_detected, "date": s.created_at} for s in recent_scans
        ]
    }