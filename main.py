import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import openai

# Charger les variables d'environnement (.env)
load_dotenv()

# Configurer la clé API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat(request: ChatRequest):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": request.prompt}
        ]
    )
    return {"response": response['choices'][0]['message']['content']}
