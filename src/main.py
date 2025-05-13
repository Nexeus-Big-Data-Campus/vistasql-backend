import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm 
from sqlmodel import SQLModel, Session
from typing import Annotated
from src.db import engine, db 
from src.crud import create_user, get_user_by_email, create_feedback, get_user_by_id
from src.dto import UserCreate, FeedbackCreate
from src.models import User
from src.security import create_jwt_token, get_current_user, get_session, verify_password 

ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
docs_url = "/docs" if ENVIRONMENT != "prod" else None
app = FastAPI(title="VistaSQL API", docs_url=docs_url, redoc_url=None)

@app.on_event("startup")
def on_startup():
    """Crea las tablas en la base de datos al iniciar."""
    SQLModel.metadata.create_all(engine)

@app.post("/sign-up", status_code=status.HTTP_201_CREATED) 
def register_user(user_data: UserCreate, session: Annotated[Session, Depends(get_session)]):
    """Registra un nuevo usuario."""
    db_user = get_user_by_email(session, user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )

    new_user = create_user(session=session, user_in=user_data)
    
    if new_user is None:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="No se pudo crear el usuario."
         )
    
    token_data = {'id': new_user.id, 'email': new_user.email, 'name': new_user.name}
    token = create_jwt_token(data=token_data)
    
    return {"access_token": token, "token_type": "bearer"}

@app.post("/sign-in")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)]
):
    """Autentica al usuario y devuelve un token de acceso."""
    user = get_user_by_email(session, email=form_data.username) 
    
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = {'id': user.id, 'email': user.email, 'name': user.name}
    token = create_jwt_token(data=token_data)

    return {"access_token": token, "token_type": "bearer"}

@app.get("/users/me", response_model=User) 
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    """Devuelve los datos del usuario autenticado."""
    
    return current_user

@app.get("/items")
async def read_items(current_user: Annotated[User, Depends(get_current_user)]):
    """Endpoint de ejemplo protegido."""
    return [{"item_id": "Foo", "owner_id": current_user.id, "owner_name": current_user.name}]

@app.post("/feedback", status_code=status.HTTP_201_CREATED)
def add_feedback(
    feedback_data: FeedbackCreate, 
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)] 
):
    """Crea una nueva entrada de feedback para el usuario autenticado."""
    
    if feedback_data.user_id != current_user.id:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes enviar feedback en nombre de otro usuario."
         )
    
    db_feedback = create_feedback(session=session, feedback=feedback_data)
    if db_feedback is None:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo guardar el feedback."
         )
    
    return db_feedback