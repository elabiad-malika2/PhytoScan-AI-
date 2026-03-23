import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.db.session import engine
from app.db.base import Base

from app.core.exceptions import PhytoScanException

# --- IMPORT DES ROUTEURS ---
from app.api.routes import auth, scans, chatbot, reports , admin

from prometheus_fastapi_instrumentator import Instrumentator



# 1. Création des tables PostgreSQL (users, plant_scans, queries, reports)
Base.metadata.create_all(bind=engine)

# 2. Création de l'App FastAPI
app = FastAPI(
    title="PhytoScan AI API",
    description="Application Agricole Intelligente (Vision par ordinateur & RAG Gemini)",
    version="1.0.0"
)

# À mettre tout à la fin de main.py, juste avant la route @app.get("/")
Instrumentator().instrument(app).expose(app)
# 3. Création des dossiers physiques (pour stocker images et PDFs)
UPLOAD_DIR = os.path.join(settings.DATA_ROOT, "uploads")
REPORTS_DIR = os.path.join(settings.DATA_ROOT, "reports")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# 4. Autoriser le Front-end (React) à lire les dossiers contenant les images et les PDF
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/reports_files", StaticFiles(directory=REPORTS_DIR), name="reports_files")

# 5. Sécurité CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# 6. Intercepteur d'Erreurs
@app.exception_handler(PhytoScanException)
async def phytoscan_exception_handler(request: Request, exc: PhytoScanException):
    headers = getattr(exc, "headers", None)
    if headers:
        return JSONResponse(status_code=exc.status_code, content={"error": exc.detail}, headers=headers)
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

# 7. INCLUSION DES 4 GRANDES ROUTES
app.include_router(auth.router, prefix="/api/v1/auth", tags=["1. Authentification"])
app.include_router(scans.router, prefix="/api/v1/scans", tags=["2. Analyse IA (Vision)"])
app.include_router(chatbot.router, prefix="/api/v1/chat", tags=["3. Chatbot (RAG Expert)"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["4. Rapports & Historique"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["5. Back-Office Administrateur"])

# 8. Health Check
@app.get("/", tags=["Système"])
def read_root():
    return {"message": "Bienvenue sur l'API PhytoScan AI 🌿. Le système est opérationnel."}