import os
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session
from typing import Annotated
from src.db import engine
from src.crud import get_user_by_email, create_user
from src.security import create_jwt_token
from src.dto import UserCreate
from datetime import timedelta

ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
dosc_url = "/docs" if ENVIRONMENT != "prod" else None
app = FastAPI(docs_url=dosc_url, redoc_url=None)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

@app.post("/sign-in")
def register_user(user: UserCreate, session: Annotated[Session, Depends(get_session)]):
    new_user = create_user(session, user)
    if new_user is None:
        raise HTTPException(status_code=400, detail="Email already exsists")

    token = create_jwt_token({
        'id': new_user.id,
        'name': new_user.name,
        'email': new_user.email,
    })
    return {"access_token": token, "token_type": "bearer"}