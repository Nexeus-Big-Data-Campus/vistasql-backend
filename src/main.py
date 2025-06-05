import os
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, Request, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import SQLModel, Session
from typing import Annotated
from models.user import User, UserSession
from src.db import engine
from src.crud import get_user_by_email, create_user, create_feedback
from src.dto import UserCreate, FeedbackCreate
from src.routes import users as users_router  
from src.routes.users import add_feedback as feedback
from src.security import create_jwt_token
from fastapi.middleware.cors import CORSMiddleware
from src.middleware.auth_middleware import auth_middleware
from src.routes import auth, session, users
from crud.user_crud import delete_user
from src.db.db import get_session

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
    
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
dosc_url = "/docs" if ENVIRONMENT != "prod" else None

app = FastAPI(docs_url=dosc_url, redoc_url=None, lifespan=lifespan)
app.include_router(users_router.router)  
app.middleware("http")(auth_middleware)
# TODO: Allow production url on prod environment
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(auth.router)
app.include_router(users.router, prefix="/users")
app.include_router(feedback.router, prefix="/feedback")
app.include_router(session.router, prefix="/session")
# app.include_router(admin.router, prefix="/admin")
