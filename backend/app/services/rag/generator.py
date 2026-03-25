import os
import mlflow
from google import genai # Nouvelle librairie Google
from app.core.config import settings
from prometheus_client import Histogram
from app.services.rag.retriever import retrieve_and_rerank

# Initialisation du client Google GenAI
client = genai.Client(api_key=settings.GEMINI_API_KEY)

# Création du Chronomètre Prometheus (Mesure le temps de réponse de l'IA)
RAG_LATENCY = Histogram('rag_generation_latency_seconds', 'Temps pris par Gemini pour répondre')



def generate_agricultural_advice(maladie_detectee: str, langue: str = "fr"):
    """Orchestre le RAG, génère la réponse, et logue TOUT dans MLFlow."""

    # Configuration MLFlow
    MLFLOW_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
    mlflow.set_tracking_uri(MLFLOW_URI)
    mlflow.set_experiment("PhytoScan_Production_RAG")
    
    # 1. On récupère les listes de contextes
    ranked_chunks, ranked_metadatas = retrieve_and_rerank(maladie_detectee)
    
    if not ranked_chunks:
        message = "Aucune information trouvée dans la base."
        return {"maladie_detectee": maladie_detectee, "rapport_ia": message, "ressource_officielle": "Vide"}

    best_chunk = ranked_chunks[0]
    source_maladie = ranked_metadatas[0].get("maladie", "Guide PhytoScan")

    # 2. Création du Prompt
    prompt = f"""
    Tu es un expert agronome travaillant pour PhytoScan AI.
    L'intelligence artificielle vient de détecter cette maladie : {maladie_detectee}.
    
    Base-toi EXCLUSIVEMENT sur le texte suivant issu de notre manuel agronomique :
    ---
    {best_chunk}
    ---
    
    Rédige un rapport clair pour l'agriculteur en langue {langue}.
    Structure ta réponse :
    1. Résumé de la maladie et gravité
    2. Symptômes
    3. Traitements (Prophylactiques et Chimiques)
    
    Sois professionnel et direct. Ne dis pas que tu es une IA.
    """
    
    # 3. Génération avec la nouvelle API Gemini
    print(" Appel à Google Gemini...")
    response = client.models.generate_content(
        model='gemini-flash-latest',
        contents=prompt
    )

   # =======================================================
    # 4. LOGGING COMPLET DANS MLFLOW (Production Tracking)
    # =======================================================
    try:
        # On essaie d'envoyer les logs à MLFlow
        with mlflow.start_run(run_name=f"Query_{maladie_detectee[:15]}", nested=True):
            mlflow.log_param("Input_Maladie", maladie_detectee)
            mlflow.log_param("Input_Langue", langue)
            mlflow.log_param("LLM_Model", "gemini-2.5-flash")
            mlflow.log_param("Retriever_Source_Top1", source_maladie)
            mlflow.log_param("Nb_Chunks_Trouves", len(ranked_chunks))
            mlflow.log_text(prompt, "prompt_envoye_au_LLM.txt")
            mlflow.log_text(response.text, "reponse_generee_par_LLM.txt")
            
            tous_les_chunks = "\n\n=== CHUNK SUIVANT ===\n\n".join(ranked_chunks)
            mlflow.log_text(tous_les_chunks, "chunks_retrouves_par_ChromaDB.txt")
            
    except Exception as e:
        # Si MLFlow plante (Erreur 403, Serveur éteint, etc.), on empêche le crash !
        print(f"⚠️ AVERTISSEMENT : Impossible de sauvegarder dans MLFlow. L'analyse continue... Erreur : {e}")

    # 5. Retour au Backend (L'agriculteur reçoit sa réponse dans tous les cas !)
    return {
        "maladie_detectee": maladie_detectee,
        "rapport_ia": response.text,
        "ressource_officielle": source_maladie
    }