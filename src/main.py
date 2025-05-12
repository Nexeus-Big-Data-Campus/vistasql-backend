# src/main.py
import os
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session
from typing import Annotated
from src.db import engine
from src.crud import get_user_by_email, create_user
from src.security import create_jwt_token
from src.dto import UserCreate
from datetime import timedeltaç
import user

ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
dosc_url = "/docs" if ENVIRONMENT != "prod" else None
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(docs_url=dosc_url, redoc_url=None, lifespan=lifespan)

def get_session():
    with Session(engine) as session:
        yield session

@app.post("/sign-in")
def register_user(user: UserCreate, session: Annotated[Session, Depends(get_session)]):
    new_user = create_user(session, user)
    if new_user is None:
        raise HTTPException(status_code=400, detail="Email already exsists")

    token = new_user.get_jtw_token()
    return {"access_token": token, "token_type": "bearer"}