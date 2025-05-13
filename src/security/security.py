import os
import jwt
from datetime import datetime, timedelta
from typing import Optional, Annotated 
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session 
from src.db import engine 
from src.models import User
from src.crud.user_crud import get_user_by_id



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24

bearer_scheme = HTTPBearer()

def create_jwt_token(data: dict):
    to_encode = data.copy()
    expiration_date = datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
    to_encode.update({"exp": expiration_date})
    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRER_KEY no esta configurada en las variables")
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def decode_jwt_token(token: str):

    try:
        if not JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY no esta configurada para decodificar")
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    
    except jwt.ExpiredSignatureError:
        
        return None
    except jwt.PyJWTError as e: 
        
        return None
    except Exception as e:
        print(f"Error inespeado al decodificar token{e}")
        return None

def get_session():
    with Session(engine) as session:
        yield session


async def get_current_user(
    
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    session: Annotated[Session, Depends(get_session)] 
) -> User:
    credential_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token= credentials.credentials

    payload = decode_jwt_token(token)
    if payload is None:
        raise credential_exception
    
    user_id: Optional[str] = payload.get("id")
    if user_id is None:
        raise credential_exception 

    
    user = get_user_by_id(session=session, user_id=user_id)
    if user is None:
        
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
        
    return user

