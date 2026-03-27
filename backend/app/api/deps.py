# Dépendances (ex: get_db, get_current_user)
# app/api/deps.py
from fastapi import Depends, HTTPException , status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.db.session import SessionLocal
from app.core.config import settings
from app.models.user import User
from app.core.exceptions import InvalidTokenException 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidTokenException()
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            raise InvalidTokenException()
    except JWTError:
        raise InvalidTokenException()

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise InvalidTokenException()

    return user


def get_current_agriculteur(current_user = Depends(get_current_user)):
    """Vérifie que l'utilisateur a bien le rôle 'agriculteur'."""
    if current_user.role != "agriculteur":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Accès refusé. Cette fonctionnalité est réservée aux agriculteurs."
        )
    return current_user

def get_current_admin(current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Accès refusé. Espace réservé aux administrateurs."
        )
    return current_user