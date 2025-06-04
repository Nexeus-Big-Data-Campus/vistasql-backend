from contextlib import asynccontextmanager
import os
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session
from src.db import engine
from src.crud import create_user, create_feedback, delete_user, get_user_by_email
from src.dto import UserCreate, FeedbackCreate
from src.dto.user import UserProfile
from src.middleware.auth_middleware import auth_middleware
from src.routes import auth, feedback, session, users, admin

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app.include_router(auth.router)
app.include_router(users.router, prefix="/users")
app.include_router(feedback.router, prefix="/feedback")
app.include_router(session.router, prefix="/session")