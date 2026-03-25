import pytest
from unittest.mock import patch

# ========================================================
# 1. TESTS D'AUTHENTIFICATION
# ========================================================
def test_register_user(client):
    """Teste si un utilisateur peut s'inscrire."""
    payload = {
        "username": "agriculteur_test",
        "email": "test@agri.com",
        "password": "password123",
        "role": "agriculteur"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    # 200 = succès, 400 = email déjà utilisé (si le test tourne 2 fois)
    assert response.status_code in [200, 400] 

def test_login_user(client):
    """Teste si l'utilisateur reçoit bien un token JWT."""
    payload = {"username": "test@agri.com", "password": "password123"}
    response = client.post("/api/v1/auth/login", data=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()

# ========================================================
# 2. TEST DU SCAN (VISION + RAG) VIA DES MOCKS !
# ========================================================
# On "Mock" (court-circuite) le modèle de Vision ET le RAG pour que ça aille très vite
@patch("app.api.routes.scans.predict_disease_from_image")
@patch("app.api.routes.scans.generate_agricultural_advice")
def test_analyze_scan_with_mocks(mock_rag, mock_vision, client):
    # 1. On dit aux Mocks quoi répondre
    mock_vision.return_value = "tomato_late_blight"
    mock_rag.return_value = {
        "maladie_detectee": "tomato_late_blight",
        "rapport_ia": "Ceci est un faux rapport généré pour le test.",
        "ressource_officielle": "Faux PDF"
    }

    # 2. On se connecte pour avoir un Token
    login_res = client.post("/api/v1/auth/login", data={"username": "test@agri.com", "password": "password123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. On envoie une fausse image à l'API
    files = {"file": ("test.jpg", b"fake_image_bytes_12345", "image/jpeg")}
    data = {"langue": "fr"}
    
    response = client.post("/api/v1/scans/analyze", headers=headers, files=files, data=data)
    
    # 4. Vérifications
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["status"] == "success"
    assert json_resp["maladie_detectee"] == "tomato_late_blight"
    assert "faux rapport" in json_resp["rapport_expert"].lower()

# ========================================================
# 3. TEST DU CHATBOT (RAG)
# ========================================================
@patch("app.api.routes.chatbot.generate_agricultural_advice")
def test_ask_chatbot_with_mocks(mock_rag, client):
    # 1. On dit au RAG quoi répondre
    mock_rag.return_value = {
        "maladie_detectee": "mildiou",
        "rapport_ia": "Utilisez de la bouillie bordelaise.",
        "ressource_officielle": "Guide PhytoScan"
    }

    # 2. On récupère le token
    login_res = client.post("/api/v1/auth/login", data={"username": "test@agri.com", "password": "password123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. On pose la question
    payload = {"question": "Comment traiter le mildiou ?", "langue": "fr"}
    response = client.post("/api/v1/chat/ask", headers=headers, json=payload)
    
    # 4. Vérifications
    assert response.status_code == 200
    assert response.json()["rapport_ia"] == "Utilisez de la bouillie bordelaise."

# ========================================================
# 4. TEST DE L'HISTORIQUE (GET)
# ========================================================
def test_get_chat_history(client):
    login_res = client.post("/api/v1/auth/login", data={"username": "test@agri.com", "password": "password123"})
    token = login_res.json()["access_token"]
    
    response = client.get("/api/v1/chat/history", headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    # On vérifie que ça renvoie bien une liste
    assert isinstance(response.json(), list)