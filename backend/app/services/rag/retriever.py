from sentence_transformers import CrossEncoder
from app.services.rag.vector_db import get_chroma_collection
from app.services.rag.embedder import get_embedding_model

_reranker = None

def get_reranker():
    global _reranker
    if _reranker is None:
        print("Chargement du modèle CrossEncoder (Reranking)...")
        _reranker = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1')
    return _reranker

def retrieve_and_rerank(query: str, top_k: int = 5):
    """Cherche les K meilleurs chunks, les re-note, et renvoie la LISTE triée."""
    print(f" Recherche du meilleur contexte pour : '{query}'")
    
    collection = get_chroma_collection()
    model = get_embedding_model()
    reranker = get_reranker()
    
    query_vector = model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_vector, n_results=top_k)
    
    if not results['documents'][0]:
        return [], []

    retrieved_docs = results['documents'][0]
    retrieved_metadatas = results['metadatas'][0]
    
    pairs = [[query, doc] for doc in retrieved_docs]
    scores = reranker.predict(pairs)
    
    # Trier du plus grand score au plus petit
    ranked_results = sorted(zip(scores, retrieved_docs, retrieved_metadatas), key=lambda x: x[0], reverse=True)
    
    ranked_chunks = [res[1] for res in ranked_results]
    ranked_metadatas = [res[2] for res in ranked_results]
    
    print(f"Chunk #1 sélectionné : {ranked_metadatas[0].get('maladie')} (Score: {ranked_results[0][0]:.2f})")
    
    return ranked_chunks, ranked_metadatas