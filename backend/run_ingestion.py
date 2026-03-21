from app.services.rag.document_loader import load_pdf_text
from app.services.rag.chunker import chunk_phytoscan_text
from app.services.rag.vector_db import ingest_documents_to_db

pdf_path = "/app/data/knowledge_base/reference_maladies_plantes.pdf"
texte_brut = load_pdf_text(pdf_path)
documents, metadatas, ids = chunk_phytoscan_text(texte_brut)
ingest_documents_to_db(documents, metadatas, ids)