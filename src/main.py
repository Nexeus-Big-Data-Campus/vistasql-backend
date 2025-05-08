from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Session, select
from src.db import engine
from src.models.user import User, create_token
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os
from src.crud.user_crud import add_user

app = FastAPI()


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/sign-in")
def register_user(name: str, email: str, password: str):
    #llamamos a la función add_user para registrar el usuario
    new_user = add_user(name, email, password)
    if new_user is None:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Generar un token JWT
    token = token = create_token(email=new_user.email, name=new_user.name)

    return {"access_token": token, "token_type": "bearer"}

@app.get("/")
def read_root():
    return {"Hello": "World"}