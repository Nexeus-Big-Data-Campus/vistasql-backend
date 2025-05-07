from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Session, select
from src.db import engine
from src.models import User
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

app = FastAPI()

# encriptar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Clave secreta para generar tokens JWT
SECRET_KEY = "Nexus2025%"  # Cambia esto por una clave segura

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/register")
def register_user(name: str, email: str, password: str):
    with Session(engine) as session:
        # Verificar si el email ya existe
        statement = select(User).where(User.email == email)
        existing_user = session.exec(statement).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="El email ya está registrado")

        # Encriptar la contraseña
        hashed_password = pwd_context.hash(password)

        # Crear un nuevo usuario
        new_user = User(name=name, email=email, password=hashed_password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        # Generar un token JWT
        token_data = {
            "sub": new_user.email,
            "name": new_user.name,
            "exp": datetime.utcnow() + timedelta(hours=1)  # Token válido por 1 hora
        }
        token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")

        return {"access_token": token, "token_type": "bearer"}

@app.get("/")
def read_root():
    return {"Hello": "World"}