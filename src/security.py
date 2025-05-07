import os
from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext
from jose import JWTError, jwt

# Configuracion de hashing de contraseñar
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuracion de JWT

SECRET_KEY = os.getenv("SECRET_KEY", "123456") #se cambia la clave despues y se usa variable de entrno
ALGORITHM = "HS256"
ACCES_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Verifica si una contraseña plana coincide con una contraseña hacheada"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) ->str:
    """Hasheada una contraseña"""

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crea un token de acceso JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """Decodifica un token acceso JWT."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

