import chromadb
from app.services.rag.embedder import get_embedding_model

CHROMA_PATH = "../data/vector_store" # Ou "/app/data/vector_store" dans Docker

def get_chroma_collection():
    """Initialise le client ChromaDB et récupère la collection."""
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_or_create_collection(name="phytoscan_knowledge")

def ingest_documents_to_db(documents: list, metadatas: list, ids: list):
    """(Ingestion) Sauvegarde les chunks dans ChromaDB."""
    print("Création des embeddings et sauvegarde dans ChromaDB...")
    model = get_embedding_model()
    embeddings = model.encode(documents).tolist()
    
    collection = get_chroma_collection()
    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    print(" Ingestion terminée avec succès !")