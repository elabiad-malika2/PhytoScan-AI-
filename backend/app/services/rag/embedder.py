from sentence_transformers import SentenceTransformer

_embedding_model = None

def get_embedding_model():
    """Retourne le modèle d'embedding multilingue (FR/EN)."""
    global _embedding_model
    if _embedding_model is None:
        print(" Chargement du modèle SentenceTransformer...")
        _embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    return _embedding_model