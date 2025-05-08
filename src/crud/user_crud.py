from src.models import User
from sqlmodel import SQLModel, Session, select
from src.db.db import engine, pwd_context
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
            existing_user = get_user_by_email(email)
            if existing_user:
                return None
        
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
            return None
        return user
    
def delete_user(email: str):
    '''
    Elimina un usuario de la base de datos dado su email.
    email: Correo electrónico del usuario
    '''
    with Session(engine) as session:
        # Buscar el usuario por email
        user = get_user_by_email(email)
        
        # Eliminar el usuario
        session.delete(user)
        session.commit()
        return {"detail": "Usuario eliminado"}

def update_user(email: str, name: str = None, password: str = None):
    '''
    Actualiza un usuario en la base de datos dado su email.
    email: Correo electrónico del usuario
    name: Nuevo nombre del usuario (opcional)
    password: Nueva contraseña del usuario (opcional)
    '''
    with Session(engine) as session:
        # Buscar el usuario por email
        user = get_user_by_email(email)
        
        # Actualizar el nombre y/o la contraseña
        if name:
            user.name = name
        if password:
            user.password = pwd_context.hash(password)
        
        session.add(user)
        session.commit()
        session.refresh(user)
        return user