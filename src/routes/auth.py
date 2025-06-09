# src/routes/auth.py
import jwt
import os
from typing import Annotated
from sqlmodel import Session
from src.crud import get_user_by_email, create_user
from src.db import get_session
from src.dto import UserCreate, UserLogin
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

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