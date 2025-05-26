from contextlib import asynccontextmanager
import os
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session
from src.db import engine
from src.crud import create_user, create_feedback, delete_user, get_user_by_email
from src.dto import UserCreate, FeedbackCreate
from src.dto.user import UserProfile
from src.middleware.auth_middleware import auth_middleware
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from src.routes import session
from fastapi.security import OAuth2PasswordRequestForm
from src.db.db import get_session as get_db
from src.security.security import create_jwt_token, verify_password, Token
from src.crud.user_crud import get_current_user
from src.models import User
from dotenv import load_dotenv
load_dotenv()


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

    token = create_jwt_token({
        "id": new_user.id,
        "email": new_user.email,
        "name": new_user.name
    })
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

#Creando el token que se genera en la sesión
@app.post("/login", response_model=Token)
async def login_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Las credenciales introducidas no son válidas")

    access_token = create_jwt_token({
        "id": user.id,
        "email": user.email,
        "name": user.name
    })
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id 
    }

#Creando un endpoint para que el usuario pueda ver sus datos      
@app.get("/profile", response_model=UserProfile)  
def get_profile(current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code= 404, detail="No se ha encontrado ningún usuario")
    
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "created_at": current_user.created_at
        }
    
#Creando el endpoint de eliminación de usuario    
@app.delete("/users/{user_id}")
def remove_user(user_id: str, session: Annotated[Session, Depends(get_session)]):
    success = delete_user(session, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

app.include_router(session.router, prefix="/session", tags=["Session"])


print("DATABASE_URL =>", os.getenv("DATABASE_URL"))
