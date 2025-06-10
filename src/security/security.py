# src/security/security.py
import os
import jwt
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from fastapi import Request
from fastapi.responses import JSONResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_jwt_token(data: dict):
    to_encode = data.copy()
    expiration_date = datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
    to_encode.update({"exp": expiration_date})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_jwt_token(token: str):
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    return payload

def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"detail":"Token no proporcionado o inválido"})
        
    token = auth_header.split(" ")[1]  # Extraer el token después de "Bearer"
    try:
        return decode_jwt_token(token)
    except jwt.exceptions.ExpiredSignatureError:
        return JSONResponse(status_code=401, detail="El token ha expirado")
    except jwt.exceptions.DecodeError:
        return JSONResponse(status_code=401, detail="Token inválido")