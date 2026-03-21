import os
from fpdf import FPDF
from datetime import datetime

# Dossier où seront stockés les PDF générés dans Docker
REPORTS_DIR = "/app/data/reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

class PhytoReportPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(34, 139, 34) # Vert forêt
        self.cell(0, 10, 'PhytoScan AI - Rapport de Diagnostic', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Genere par Intelligence Artificielle - Page {self.page_no()}', 0, 0, 'C')

def generate_diagnostic_pdf(username: str, maladie: str, rapport_texte: str, image_path: str = None) -> str:
    """Crée le PDF, y insère le texte et l'image, et retourne le chemin d'accès."""
    pdf = PhytoReportPDF()
    pdf.add_page()
    
    # 1. Informations de l'agriculteur
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f"Agriculteur : {username}", 0, 1)
    pdf.cell(0, 8, f"Date d'analyse : {datetime.now().strftime('%d/%m/%Y a %H:%M')}", 0, 1)
    pdf.ln(5)

    # 2. Résultat de la Vision IA
    pdf.set_font("Arial", 'B', 14)
    if "healthy" in maladie.lower():
        pdf.set_text_color(0, 150, 0) # Vert si sain
    else:
        pdf.set_text_color(200, 0, 0) # Rouge si malade
        
    pdf.cell(0, 10, f"Diagnostic IA : {maladie.upper()}", 0, 1)
    pdf.ln(5)

    # 3. Insertion de la photo scannée (Si elle existe)
    if image_path and os.path.exists(image_path):
        # On centre l'image (X=65, Largeur=80)
        pdf.image(image_path, x=65, w=80)
        pdf.ln(5) # Espace sous l'image

    # 4. Le Rapport RAG (Gemini)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Conseils Agronomiques :", 0, 1)
    
    pdf.set_font("Arial", '', 11)
    # Remplacement des caractères spéciaux pour éviter les erreurs FPDF
    texte_propre = rapport_texte.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, texte_propre)

    # Sauvegarde du fichier
    filename = f"rapport_{username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    filepath = os.path.join(REPORTS_DIR, filename)
    pdf.output(filepath)
    
    return filepath