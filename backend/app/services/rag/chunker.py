import re

def chunk_phytoscan_text(full_text: str):
    """Découpe le texte par maladie et prépare les métadonnées pour ChromaDB."""
    print(" Découpage du texte en cours...")
    raw_chunks = re.split(r'\n(?=[IVX]+\.\s)', full_text)
    
    documents = []
    metadatas = []
    ids = []
    
    for i, chunk in enumerate(raw_chunks):
        chunk = chunk.strip()
        if len(chunk) < 50: 
            continue # Ignorer l'intro
            
        titre = "Général"
        match = re.search(r'^[IVX]+\.\s(.*?)\n', chunk)
        if match:
            titre = match.group(1).strip()
            
        documents.append(chunk)
        metadatas.append({"maladie": titre, "source": "Guide PhytoScan"})
        ids.append(f"maladie_chunk_{i}")
        
    print(f" {len(documents)} maladies chunkées.")
    return documents, metadatas, ids