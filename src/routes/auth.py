# src/routes/auth.py
import jwt
import os
from typing import Annotated
from sqlmodel import Session
from src.crud import get_user_by_email, create_user
from src.db import get_session
from src.dto import UserCreate, UserLogin
from src.models import User
from src.security.security import decode_jwt_token
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")
ALGORITHM = "HS256"

@router.post("/signin")
def register_user(user: UserCreate, session: Annotated[Session, Depends(get_session)]):
    new_user = create_user(session, user)
    if new_user is None:
        raise HTTPException(status_code=400, detail="Email already exsists")

    token = new_user.get_jwt_token()
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
def login_user(login: UserLogin, session: Annotated[Session, Depends(get_session)]):
    user = get_user_by_email(session, login.email)
    if user is None or not user.verify_password(login.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = user.get_jwt_token()
    return {"access_token": token, "token_type": "bearer"}
    
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_jwt_token(token)
        user_id: str = payload.get("id")
        if user_id is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise credentials_exception
    
    user = session.get(User, user_id)
    if user is None:
        raise credentials_exception
    return {"access_token": token, "token_type": "bearer"}