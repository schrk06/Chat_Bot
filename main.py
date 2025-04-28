"""import os
from fastapi import FastAPI, Depends, HTTPException
from auth import create_access_token, authenticate_user, verify_token, oauth2_scheme, fake_user_db
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from transformers import pipeline
from fastapi.responses import JSONResponse
from typing import Optional

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

app = FastAPI()

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
"""

import os
from fastapi import FastAPI, Depends, HTTPException
from auth import create_access_token, authenticate_user, verify_token, oauth2_scheme, fake_user_db
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

class User(BaseModel):
    username: str
    password: str

class ChatRequest(BaseModel):
    prompt: str



# Route pour s'inscrire (simulé ici)
@app.post("/register")
def register(user: User):
    if user.username in fake_user_db:
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant.")
    fake_user_db[user.username] = {"username": user.username, "password": user.password}
    return {"message": "Inscription réussie."}

#Connexion 
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
    verify_token(token)  
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