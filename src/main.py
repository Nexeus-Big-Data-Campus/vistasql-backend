import os
from fastapi import FastAPI, Depends, HTTPException, Request, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import SQLModel, Session
from typing import Annotated
from src.db import engine
from src.crud import create_user, create_feedback
from src.dto import UserCreate, FeedbackCreate
from src.routes import auth
from src.db.db import get_session
from src.middleware.auth_middleware import auth_middleware  # ← también lo añadimos

ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
dosc_url = "/docs" if ENVIRONMENT != "prod" else None
app = FastAPI(docs_url=dosc_url, redoc_url=None)


app.include_router(auth.router)
security = HTTPBearer()
app.middleware("http")(auth_middleware)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/sign-in")
def register_user(user: UserCreate, session: Annotated[Session, Depends(get_session)]):
    new_user = create_user(session, user)
    if new_user is None:
        raise HTTPException(status_code=400, detail="Email already exsists")

    token = new_user.get_jwt_token()
    return {"access_token": token, "token_type": "bearer"}

@app.post("/feedback")
def add_feedback(
    feedback: FeedbackCreate,
    session: Annotated[Session, Depends(get_session)],
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    return create_feedback(session, feedback)
