from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from sqlmodel import SQLModel
from src.db import engine
from src.crud import create_user, create_feedback, delete_user
from src.dto import UserCreate, FeedbackCreate
from src.middleware.auth_middleware import auth_middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, HTTPException
from typing import Annotated
from sqlmodel import Session
from src.routes import session
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.db.db import get_session as get_db
from src.security.security import create_jwt_token, verify_password, Token
from src.crud import get_user_by_email

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
    
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
dosc_url = "/docs" if ENVIRONMENT != "prod" else None
app = FastAPI(docs_url=dosc_url, redoc_url=None, lifespan=lifespan)

app.middleware("http")(auth_middleware)
# TODO: Allow production url on prod environment
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=["*"], allow_methods=["*"], allow_headers=["*"])

def get_session():
    with Session(engine) as session:
        yield session

@app.post("/sign-in")
def register_user(user: UserCreate, session: Annotated[Session, Depends(get_session)]):
    new_user = create_user(session, user)
    if new_user is None:
        raise HTTPException(status_code=400, detail="Email already exists")

    token = new_user.get_jwt_token()
    return {
        "id": new_user.id, 
        "access_token": token,
        "token_type": "bearer"
    }


@app.post("/feedback")
def add_feedback(
    feedback: FeedbackCreate,
    session: Annotated[Session, Depends(get_session)],
):
    return create_feedback(session, feedback)

@app.post("/token", response_model=Token)
async def login_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_jwt_token({
        "id": user.id,
        "email": user.email,
        "name": user.name
    })
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id  # Puedes quitar esto si no está en tu modelo de respuesta
    }


@app.delete("/users/{user_id}")
def remove_user(user_id: str, session: Annotated[Session, Depends(get_session)]):
    success = delete_user(session, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

app.include_router(session.router, prefix="/session", tags=["Session"])


print("DATABASE_URL =>", os.getenv("DATABASE_URL"))
