from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_admin
from app.models.user import User
from app.schemas.user_schema import UserResponse
from app.dal.admin_dal import get_all_agriculteurs, delete_user_by_id, get_platform_statistics

router = APIRouter()

@router.get("/dashboard", summary="Statistiques de la plateforme")
def get_admin_dashboard(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin) 
):
    """Renvoie les chiffres clés de PhytoScan AI."""
    return get_platform_statistics(db)

@router.get("/users", response_model=List[UserResponse], summary="Liste des agriculteurs")
def list_agriculteurs(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Renvoie la liste de tous les agriculteurs inscrits."""
    return get_all_agriculteurs(db)

@router.delete("/users/{user_id}", summary="Supprimer un agriculteur")
def remove_agriculteur(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Bannit un utilisateur et supprime toutes ses données (Scans, Historique)."""
    # Empêcher l'admin de se suicider (se supprimer lui-même)
    if user_id == current_admin.id:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas supprimer votre propre compte Admin.")

    deleted_user = delete_user_by_id(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable.")
        
    return {"message": f"L'agriculteur {deleted_user.username} a été supprimé avec succès."}