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
    
    # 1. Vérification de sécurité (Le scan existe-t-il et appartient-il à l'utilisateur ?)
    scan = db.query(PlantScan).filter(PlantScan.id == scan_id, PlantScan.user_id == current_user.id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan introuvable ou non autorisé.")

    # 2. Récupération du texte généré par Gemini (Le Rapport)
    report = db.query(Report).filter(Report.scan_id == scan_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Aucune recommandation n'a été générée pour ce scan.")

    # 3. Si le PDF existe DÉJÀ sur le serveur, on l'envoie tout de suite (Rapide !)
    if report.pdf_path and os.path.exists(f"/app/data{report.pdf_path}"):
        return FileResponse(
            path=f"/app/data{report.pdf_path}", 
            media_type='application/pdf', 
            filename=f"Diagnostic_{scan.disease_detected}.pdf"
        )

    # 4. S'il n'existe pas, on le GÉNÈRE
    absolute_image_path = f"/app/data{scan.image_path}" # Ex: /app/data/uploads/image.jpg
    
    pdf_filepath = generate_diagnostic_pdf(
        username=current_user.username,
        maladie=scan.disease_detected,
        rapport_texte=report.treatment_recommendation,
        image_path=absolute_image_path if os.path.exists(absolute_image_path) else None
    )

    # 5. On met à jour la base de données pour se souvenir d'où est stocké le PDF
    report.pdf_path = pdf_filepath.replace("/app/data", "") # On stocke un chemin web relatif
    db.commit()

    # 6. On l'envoie à l'utilisateur
    return FileResponse(
        path=pdf_filepath, 
        media_type='application/pdf', 
        filename=f"Diagnostic_{scan.disease_detected}.pdf"
    )