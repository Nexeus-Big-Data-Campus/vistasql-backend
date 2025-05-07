from src.models import User
from sqlmodel import SQLModel, Session, select
from src.db import engine
from passlib.context import CryptContext
from fastapi import FastAPI, HTTPException

def add_user(name: str, email: str, password: str):
    '''
    Registra un nuevo usuario en la base de datos.
    name: Nombre del usuario
    email: Correo electrónico del usuario
    password: Contraseña del usuario
    '''
    # Encriptar contraseña
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
            return new_user

def get_user_by_email(email: str):
    '''
    Obtiene un usuario de la base de datos dado su email.
    email: Correo electrónico del usuario
    '''
    with Session(engine) as session:
        # Buscar el usuario por email
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    
