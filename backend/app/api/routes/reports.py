import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user,get_current_agriculteur
from app.models.user import User
from app.models.plant_scan import PlantScan
from app.models.report import Report

from app.services.pdf_service import generate_diagnostic_pdf
from app.schemas.scan_schema import ScanHistoryResponse

router = APIRouter()

@router.get("/history",response_model=List[ScanHistoryResponse])
def get_user_scan_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_agriculteur)
):
    """Renvoie la liste de toutes les plantes scannées par l'agriculteur (Dashboard)."""
    scans = db.query(PlantScan).filter(PlantScan.user_id == current_user.id).order_by(PlantScan.created_at.desc()).all()
    return scans

@router.get("/download/{scan_id}")
def download_report_pdf(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_agriculteur)
):
    """Génère (si besoin) et télécharge le rapport PDF d'un scan spécifique."""
    
    scan = db.query(PlantScan).filter(PlantScan.id == scan_id, PlantScan.user_id == current_user.id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan introuvable ou non autorisé.")

    report = db.query(Report).filter(Report.scan_id == scan_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Aucune recommandation n'a été générée pour ce scan.")

    # PDF existe deja sur le serveur on l'envoie tout de suite 
    if report.pdf_path and os.path.exists(f"/app/data{report.pdf_path}"):
        return FileResponse(
            path=f"/app/data{report.pdf_path}", 
            media_type='application/pdf', 
            filename=f"Diagnostic_{scan.disease_detected}.pdf"
        )

    #  S'il n'existe pas on le genere
    absolute_image_path = f"/app/data{scan.image_path}" 
    
    pdf_filepath = generate_diagnostic_pdf(
        username=current_user.username,
        maladie=scan.disease_detected,
        rapport_texte=report.treatment_recommendation,
        image_path=absolute_image_path if os.path.exists(absolute_image_path) else None
    )

    report.pdf_path = pdf_filepath.replace("/app/data", "") 
    db.commit()

    return FileResponse(
        path=pdf_filepath, 
        media_type='application/pdf', 
        filename=f"Diagnostic_{scan.disease_detected}.pdf"
    )