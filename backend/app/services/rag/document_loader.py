import fitz  # PyMuPDF
import os

def load_pdf_text(pdf_path: str) -> str:
    """Charge un PDF et retourne le texte complet fusionné."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Fichier introuvable : {pdf_path}")
        
    print(f"📄 Chargement du document : {pdf_path}")
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text