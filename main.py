import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from transformers import pipeline
from fastapi.responses import PlainTextResponse
from fastapi.responses import JSONResponse


load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

app = FastAPI()


# Crée une pipeline pour la génération de texte
generator = pipeline('text-generation', model='distilgpt2')

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
async def root():
    return {"message": "Bienvenue sur mon chatbot API 🚀"}

@app.post("/chat")
async def chat(request: ChatRequest):
    # Utilise le modèle Hugging Face pour générer une réponse
    prompt = request.prompt
    response = generator(prompt, max_length=50, num_return_sequences=1)
    print(response)
    # Récupère la réponse générée
    generated_text = response[0]['generated_text']
    
    PlainTextResponse(content=generated_text, media_type="text/plain; charset=utf-8")

    return JSONResponse(
            content={"response": generated_text},
            media_type="application/json; charset=utf-8",
        )


