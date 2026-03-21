# Requêtes SQL liées aux analyses
from sqlalchemy.orm import Session
from app.models.plant_scan import PlantScan

def save_scan_result(db: Session, user_id: int, image_path: str, disease: str):
    """Sauvegarde l'analyse de la plante dans la BDD."""
    new_scan = PlantScan(
        user_id=user_id,
        image_path=image_path,
        disease_detected=disease
    )
    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)
    return new_scan