import os
import jwt
from datetime import datetime, timedelta
from typing import Optional, Annotated
from passlib.context import CryptContext
from fastapi import Depends, HTTPException,status, FastAPI, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from pydantic import BaseModel
from src.db.db import get_session
from src.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

app = FastAPI()

router = APIRouter()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_jwt_token(data: dict):
    to_encode = data.copy()
    expiration_date = datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
    to_encode.update({"exp": expiration_date, "sub":data.get("email")})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_jwt_token(token: str):
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    return payload
    





