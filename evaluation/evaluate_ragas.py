import sys
import os

# 🛠️ HACK CHEMIN PYTHON : Autorise l'importation du dossier "app"
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json

import numpy as np
import mlflow
from datasets import Dataset
from ragas import evaluate

# Métriques « legacy » (ragas.metrics.base.Metric) : seules acceptées par evaluate().
# evaluate() injecte llm / embeddings sur ces instances si elles sont encore None.
# Les classes de ragas.metrics.collections ne sont PAS des Metric → TypeError si on les passe en liste.
from ragas.metrics._answer_relevance import answer_relevancy
from ragas.metrics._context_precision import context_precision
from ragas.metrics._context_recall import context_recall
from ragas.metrics._faithfulness import faithfulness
from ragas.llms import llm_factory
from openai import OpenAI

# answer_relevancy (métrique legacy) appelle embed_query() — interface LangChain, pas l’embedder natif RAGAS.
from langchain_community.embeddings import HuggingFaceEmbeddings

# 3. Imports de ton RAG Backend
from app.services.rag.retriever import retrieve_and_rerank
from app.services.rag.generator import generate_agricultural_advice


# Noms affichés dans MLflow (les clés RAGAS sont en snake_case, ex. answer_relevancy)
_MLFLOW_METRIC_LABELS = {
    "faithfulness": "Faithfulness",
    "answer_relevancy": "Answer_Relevancy",
    "context_precision": "Context_Precision",
    "context_recall": "Context_Recall",
}


def _coerce_score_cell(v):
    """Version sans clé dict (évite bug de closure)."""
    if v is None:
        return None
    if isinstance(v, (bool, np.bool_)):
        return float(v)
    if isinstance(v, (int, float, np.floating, np.integer)):
        x = float(v)
        return None if np.isnan(x) or np.isinf(x) else x
    if isinstance(v, dict):
        for k in ("score", "value"):
            if k in v:
                return _coerce_score_cell(v[k])
        return None
    try:
        x = float(v)
        return None if np.isnan(x) or np.isinf(x) else x
    except (TypeError, ValueError):
        return None


def _mean_column(rows: list, key: str) -> float:
    """Moyenne d'une colonne dans la liste de dicts scores (ignore les NaN)."""
    vals = []
    for row in rows:
        v = _coerce_score_cell(row.get(key))
        if v is not None:
            vals.append(v)
    if not vals:
        return 0.0
    arr = np.asarray(vals, dtype=np.float64)
    if not np.any(np.isfinite(arr)):
        return 0.0
    m = float(np.nanmean(arr))
    if np.isnan(m) or np.isinf(m):
        return 0.0
    return m


def log_ragas_scores_to_mlflow(result) -> None:
    """Enregistre toutes les métriques présentes dans result.scores (évite clés erronées / oublis)."""
    rows = getattr(result, "scores", None) or []
    if not rows:
        print(" Aucun score RAGAS à envoyer à MLflow.")
        return
    keys = list(rows[0].keys())
    print(f" Colonnes de scores RAGAS : {keys}")
    print(f"   (ligne 0, bruts) {rows[0]}")
    for key in keys:
        label = _MLFLOW_METRIC_LABELS.get(key, key)
        value = _mean_column(rows, key)
        mlflow.log_metric(label, value)
        print(f"   {label} = {value}")


# =======================================================
# 1. CONFIGURATION SIMPLE DES JUGES
# =======================================================
print(" Initialisation du Juge Ollama (phi3)...")
# API compatible OpenAI : /v1 (voir https://github.com/ollama/ollama/blob/main/docs/openai.md)
_ollama_base = os.environ.get(
    "OLLAMA_OPENAI_BASE_URL", "http://host.docker.internal:11434/v1"
)
juge_llm = llm_factory(
    "phi3",
    client=OpenAI(base_url=_ollama_base, api_key=os.environ.get("OLLAMA_API_KEY", "ollama")),
)

print(" Chargement du modèle d'Embeddings (pour l'évaluation)...")
juge_embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
)


# =======================================================
# 2. PRÉPARATION DU DATASET
# =======================================================
print(" Chargement du JSON de test...")
with open("/app/evaluation/deepeval_tests/dataset.json", "r", encoding="utf-8") as f:
    test_cases = json.load(f)

questions, answers, contexts, ground_truths = [], [], [], []

print(" Ton IA (Gemini + ChromaDB) génère les réponses...")
for case in test_cases:
    q = case["input"]
    print(f"   -> Traitement de la question : '{q}'")
    
    chunks_trouves, _ = retrieve_and_rerank(q, top_k=3)
    rag_result = generate_agricultural_advice(maladie_detectee=q, langue="fr")
    
    questions.append(q)
    answers.append(rag_result["rapport_ia"])
    contexts.append(chunks_trouves)
    ground_truths.append(case["expected_output"])

dataset = Dataset.from_dict({
    "question": questions,
    "answer": answers,
    "contexts": contexts,
    "ground_truth": ground_truths
})


# =======================================================
# 3. L'ÉVALUATION RAGAS
# =======================================================
print("\n⚖️ Ollama évalue les réponses de Gemini. Cela peut prendre quelques minutes...")
metriques_a_evaluer = [
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
]

resultats = evaluate(
    dataset=dataset,
    metrics=metriques_a_evaluer,
    llm=juge_llm,
    embeddings=juge_embeddings,
)

print("\n RÉSULTATS GLOBAUX :")
print(resultats)


# =======================================================
# 4. ENREGISTREMENT DANS MLFLOW
# =======================================================
print("\n Sauvegarde des scores dans MLFlow...")
mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("PhytoScan_Ragas_Evaluation")

with mlflow.start_run(run_name="Evaluation_Automatique_Ragas"):
    log_ragas_scores_to_mlflow(resultats)

    mlflow.log_param("Evaluateur_LLM", "Ollama (phi3)")
    mlflow.log_param("Nb_Questions_Testees", len(test_cases))
    
    print(" Scores envoyés à MLFlow avec succès ! (http://localhost:5000)")