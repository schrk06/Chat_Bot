from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app, fake_user_db

client = TestClient(app)

def get_token(username="testuser", password="testpass"):
    # Inscription
    if username not in fake_user_db:
        client.post("/register", json={"username": username, "password": password})
    
    # Connexion
    response = client.post("/login", json={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]
    return token


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue sur mon chatbot API 🚀"}


def test_chat_huggingface():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/chat", json={"prompt": "Salut toi", "provider": "huggingface"}, headers=headers)
    assert response.status_code == 200
    assert "response" in response.json()
    assert isinstance(response.json()["response"], str)


@patch("main.client.chat.completions.create")
def test_chat_openai(mock_create):
    mock_create.return_value = {
        "choices": [
            {
                "message": {
                    "content": "Salut, je suis un bot !"
                }
            }
        ]
    }
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/chat", json={"prompt": "Qui es-tu ?", "provider": "openai"}, headers=headers)
    assert response.status_code == 200
    assert "Salut" in response.json()["response"]
