import os
from fastapi import FastAPI, Depends, HTTPException
from auth import create_access_token, authenticate_user, verify_token, oauth2_scheme, fake_user_db
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from transformers import pipeline
from fastapi.responses import JSONResponse
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")  #Ne sert un peu à rien pour l'instant car j'ai utilisé finalement hugginface comme provider.
client = OpenAI(api_key=api_key)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["http://localhost:5173"] si tu veux être plus restrictif
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


generator = pipeline('text-generation', model='distilgpt2')

class User(BaseModel):
    username: str
    password: str

class ChatRequest(BaseModel):
    prompt: str
    provider: Optional[str] = "huggingface"  # Ajout : choisir modèle utilisé


@app.post("/register")
def register(user: User):
    if user.username in fake_user_db:
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant.")
    fake_user_db[user.username] = {"username": user.username, "password": user.password}
    return {"message": "Inscription réussie."}


@app.post("/login")
def login(user: User):
    authenticated_user = authenticate_user(user.username, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/")
async def root():
    return {"message": "Bienvenue sur mon chatbot API 🚀"}


@app.post("/chat")
async def chat(request: ChatRequest, token: str = Depends(oauth2_scheme)):
    try:
        verify_token(token)  
        prompt = request.prompt
        response = generator(prompt, max_length=50, num_return_sequences=1)
        generated_text = response[0]['generated_text']

        return JSONResponse(
            content={"response": generated_text},
            media_type="application/json; charset=utf-8",
        )
    except Exception as e:
        print("Erreur dans /chat:", e)
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")

