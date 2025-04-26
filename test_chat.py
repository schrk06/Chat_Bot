from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue sur mon chatbot API 🚀"}

def test_chat_endpoint():
    response = client.post("/chat", json={"prompt": "Bonjour, qui es-tu ?"})
    assert response.status_code == 200
    assert "response" in response.json()
    assert isinstance(response.json()["response"], str)

@patch("main.client.chat.completions.create")
def test_chat_endpoint(mock_create):
    # Simuler une réponse d'OpenAI
    mock_create.return_value = {
        "choices": [
            {
                "message": {
                    "content": "Bonjour ! Je suis un assistant virtuel."
                }
            }
        ]
    }

    response = client.post("/chat", json={"prompt": "Bonjour, qui es-tu ?"})
    assert response.status_code == 200
    assert "Bonjour" in response.json()["response"]
