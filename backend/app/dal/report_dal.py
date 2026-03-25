# Requêtes SQL liées aux rapports
from sqlalchemy.orm import Session
from app.models.report import Report

def create_report(db: Session, scan_id: int, recommendation: str, pdf_path: str = None):
    """Crée un nouveau rapport lié à un scan dans la BDD."""
    new_report = Report(
        scan_id=scan_id,
        treatment_recommendation=recommendation,
        pdf_path=pdf_path
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report

def get_report_by_scan_id(db: Session, scan_id: int):
    """Récupère un rapport spécifique à partir de l'ID du scan."""
    return db.query(Report).filter(Report.scan_id == scan_id).first()

def get_report_by_id(db: Session, report_id: int):
    """Récupère un rapport spécifique à partir de son propre ID."""
    return db.query(Report).filter(Report.id == report_id).first()