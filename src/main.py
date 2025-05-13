# src/main.py
import os
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session
from typing import Annotated
from src.db import engine
from src.crud import get_user_by_email, create_user
from src.security import create_jwt_token
from src.dto import UserCreate
from datetime import datetime
from user import User, UserSession

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
    # Ingresar un nuevo usuario
    new_user = create_user(session, user)
    if new_user is None:
        raise HTTPException(status_code=400, detail="Email already exsists")
    
    token = new_user.get_jtw_token()
    return {"access_token": token, "token_type": "bearer"}

@app.post("/sign-out")
def logout_user(user_id: int, session: Annotated[Session, Depends(get_session)]):
    user_session = session.query(UserSession).filter(
        UserSession.user_id == user_id, UserSession.end_time == None
    ).first()

    if user_session:
        user_session.end_time = datetime.now(datetime.timezone.utc)
        user_session.duration = int((user_session.end_time - user_session.start_time).total_seconds())
        session.commit()

    return {"message": "User logged out successfully"}



@app.get("/user-sessions/{user_id}")
def get_user_sessions(user_id: int, session: Annotated[Session, Depends(get_session)]):
    #Obtener las sesiones del usuario
    sessions = session.query(UserSession).filter(UserSession.user_id == user_id).all()
    return sessions

@app.get("/user-actions/{user_id}")
def get_user_actions(user_id: int, session: Annotated[Session, Depends(get_session)]):
    # Obtener las acciones del usuario
    actions = session.query(UserAction).filter(UserAction.user_id == user_id).all()
    return actions