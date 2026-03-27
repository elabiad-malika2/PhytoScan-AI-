import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException,Form
from sqlalchemy.orm import Session
from datetime import datetime

from app.api.deps import get_db, get_current_user,get_current_agriculteur
from app.core.config import settings
from app.models.user import User

from app.services.vision_service import predict_disease_from_image
from app.services.rag.generator import generate_agricultural_advice

from app.dal.scan_dal import save_scan_result

from app.dal.report_dal import create_report
from app.schemas.scan_schema import ScanAnalyzeResponse 


router = APIRouter()

UPLOAD_DIR = os.path.join(settings.DATA_ROOT, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True) 

@router.post("/analyze",response_model=ScanAnalyzeResponse)
async def analyze_plant_image(
    file: UploadFile = File(...),
    langue: str = Form("fr"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_agriculteur) 
):

    try:
        image_bytes = await file.read()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"user_{current_user.id}_{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)
        
        with open(file_path, "wb") as buffer:
            buffer.write(image_bytes)

        maladie_predite = predict_disease_from_image(image_bytes)

        if "healthy" in maladie_predite.lower():
            rapport = "Votre plante est en excellente santé. Continuez vos bonnes pratiques agricoles (arrosage régulier, surveillance)."
            source = "Analyse IA"
        else:
            rag_result = generate_agricultural_advice(maladie_detectee=maladie_predite, langue=langue)
            rapport = rag_result.get("rapport_ia", "Erreur lors de la génération du rapport.")
            source = rag_result.get("ressource_officielle", "Inconnue")

        db_scan=save_scan_result(
            db=db,
            user_id=current_user.id,
            image_path=file_path,
            disease=maladie_predite
        )
        create_report(
            db=db,
            scan_id=db_scan.id,
            recommendation=rapport,
            pdf_path=None 
        )

        return {
            "status": "success",
            "scan_id": db_scan.id,
            "maladie_detectee": maladie_predite,
            "rapport_expert": rapport,
            "source": source,
            "image_url": f"/uploads/{safe_filename}" 
        }

    except Exception as e:
        import traceback          
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse : {str(e)}")