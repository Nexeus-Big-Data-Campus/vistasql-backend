from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Session, select
from src.db import engine
from src.models import User
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from src.crud.user_crud import add_user

app = FastAPI()

# encriptar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()

# recuperamos la clave secreta del entorno
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/register")
def register_user(name: str, email: str, password: str):
    #llamamos a la función add_user para registrar el usuario
    new_user = add_user(name, email, password)

        # Generar un token JWT
    token_data = {
        "email": new_user.email,
        "name": new_user.name,
        "exp": datetime.utcnow() + timedelta(hours=24)  # Token válido por 24 horas
    }
    token = jwt.encode(token_data, JWT_SECRET_KEY, algorithm="HS256")

    return {"access_token": token, "token_type": "bearer"}

@app.get("/")
def read_root():
    return {"Hello": "World"}