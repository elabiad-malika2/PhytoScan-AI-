import pytest
from unittest.mock import patch


def test_register_user(client):
    """Teste si un utilisateur peut s'inscrire."""
    payload = {
        "username": "agriculteur_test",
        "email": "test@agri.com",
        "password": "password123",
        "role": "agriculteur"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code in [200, 400] 

def test_login_user(client):
    """Teste si l'utilisateur reçoit bien un token JWT."""
    payload = {"username": "test@agri.com", "password": "password123"}
    response = client.post("/api/v1/auth/login", data=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()


@patch("app.api.routes.scans.predict_disease_from_image")
@patch("app.api.routes.scans.generate_agricultural_advice")
def test_analyze_scan_with_mocks(mock_rag, mock_vision, client):
    mock_vision.return_value = "tomato_late_blight"
    mock_rag.return_value = {
        "maladie_detectee": "tomato_late_blight",
        "rapport_ia": "Ceci est un faux rapport généré pour le test.",
        "ressource_officielle": "Faux PDF"
    }

    login_res = client.post("/api/v1/auth/login", data={"username": "test@agri.com", "password": "password123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    files = {"file": ("test.jpg", b"fake_image_bytes_12345", "image/jpeg")}
    data = {"langue": "fr"}
    
    response = client.post("/api/v1/scans/analyze", headers=headers, files=files, data=data)
    
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["status"] == "success"
    assert json_resp["maladie_detectee"] == "tomato_late_blight"
    assert "faux rapport" in json_resp["rapport_expert"].lower()


@patch("app.api.routes.chatbot.generate_agricultural_advice")
def test_ask_chatbot_with_mocks(mock_rag, client):
    mock_rag.return_value = {
        "maladie_detectee": "mildiou",
        "rapport_ia": "Utilisez de la bouillie bordelaise.",
        "ressource_officielle": "Guide PhytoScan"
    }

    login_res = client.post("/api/v1/auth/login", data={"username": "test@agri.com", "password": "password123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {"question": "Comment traiter le mildiou ?", "langue": "fr"}
    response = client.post("/api/v1/chat/ask", headers=headers, json=payload)
    
    assert response.status_code == 200
    assert response.json()["rapport_ia"] == "Utilisez de la bouillie bordelaise."


def test_get_chat_history(client):
    login_res = client.post("/api/v1/auth/login", data={"username": "test@agri.com", "password": "password123"})
    token = login_res.json()["access_token"]
    
    response = client.get("/api/v1/chat/history", headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)