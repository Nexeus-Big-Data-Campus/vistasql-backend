from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import SQLModel, Session
from typing import Annotated

from src.db import engine # Importamos el motor de la base de datos
from src.models.user import User, UserCreate, Token # Importamos los modelos necesarios
from src.crud import get_user_by_email, create_user # Importamos las funciones CRUB
from src.security import create_access_token # Importamos la funcion crear token JWT
from datetime import timedelta # Neceario para la expiracion del token

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine) # Crea las tablas si no existen

def get_session():
    """Dependencia para obtener una session de base de datos"""
    with Session(engine) as session:
        yield session

@app.get("/")
def read_root():
    return{"hoLa": "mundo"}

# Nuevo endpoint para el regristro de usuarios
@app.post("/register", response_model=Token) #el endpoiunt acepta el POST y devuelve un objeto Token
def register_user(
    user: UserCreate, # Recibe los datos del usuario segun el modelo UserCreate
    session: Annotated[Session, Depends(get_session)] # Obtiene una sesion de la BD
):
    """
    Registra un nuevo usuario en la base de datos.
    - Verifica si el email ya esta registrado.
    - Hashea la contrasela.
    - Almacena el usuario en la base de datos.
    - Devuelve un token JWT.
    """
    # 1. Verifica si el email existe
    db_user = get_user_by_email(session, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "El email ya esta registrado"
        )
    # 2. crear el usuario en la base de datos (la contraseña se hashea dentro de create_user)
    created_user = create_user(session, user_in=user)

    # 3. Generar el token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": created_user.email}, # usamos el email como objeto del token
        expires_delta=access_token_expires
    ) 

    # 4. Devolver el token
    return Token(access_token=access_token, token_type="bearer")