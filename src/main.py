# src/main.py
import os
from fastapi import FastAPI, Depends, HTTPException, status # Añadir status si no estaba
from fastapi.security import OAuth2PasswordRequestForm # Para un endpoint de login estándar
from sqlmodel import SQLModel, Session
from typing import Annotated

# Importaciones de tu proyecto
from src.db import engine, db # Asumiendo que tienes db.py con engine
from src.core.hashing import verify_password # Necesario para login
from src.crud import create_user, get_user_by_email, create_feedback, get_user_by_id # get_user_by_id puede no ser necesario aquí directamente
from src.dto import UserCreate, FeedbackCreate
from src.models import User
# Importar funciones de seguridad necesarias
from src.security import create_jwt_token, get_current_user, get_session # Asegúrate que get_session esté disponible

# Configuración de la App FastAPI
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
docs_url = "/docs" if ENVIRONMENT != "prod" else None # Corregido el nombre de variable
app = FastAPI(title="VistaSQL API", docs_url=docs_url, redoc_url=None)

@app.on_event("startup")
def on_startup():
    """Crea las tablas en la base de datos al iniciar."""
    SQLModel.metadata.create_all(engine)

# --- Endpoint de Registro (Sign-Up) ---
@app.post("/sign-up", status_code=status.HTTP_201_CREATED) # Usar /sign-up para claridad, devolver 201
def register_user(user_data: UserCreate, session: Annotated[Session, Depends(get_session)]):
    """Registra un nuevo usuario."""
    db_user = get_user_by_email(session, user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )

    new_user = create_user(session=session, user_in=user_data)
    # create_user ahora devuelve Optional[User], podría devolver None si falla
    # Aunque la verificación de email ya se hizo, es bueno manejarlo
    if new_user is None:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, # O 400 si el email ya existía y create_user devuelve None por eso
            detail="No se pudo crear el usuario."
         )

    # Crear el token JWT directamente aquí
    token_data = {'id': new_user.id, 'email': new_user.email, 'name': new_user.name}
    token = create_jwt_token(data=token_data)

    # Devolver solo el token (o más info si se desea, pero no el objeto User completo)
    return {"access_token": token, "token_type": "bearer"}


# --- Endpoint de Login (Sign-In) ---
# Es más estándar usar OAuth2PasswordRequestForm para login
@app.post("/sign-in")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)]
):
    """Autentica al usuario y devuelve un token de acceso."""
    user = get_user_by_email(session, email=form_data.username) # form_data usa 'username' para el email/id

    # Verificar si el usuario existe y la contraseña es correcta
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Crear el token JWT
    token_data = {'id': user.id, 'email': user.email, 'name': user.name}
    token = create_jwt_token(data=token_data)

    return {"access_token": token, "token_type": "bearer"}


# --- Endpoint Protegido: Obtener datos del usuario actual ---
@app.get("/users/me", response_model=User) # Puedes usar response_model para filtrar datos
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    """Devuelve los datos del usuario autenticado."""
    # current_user ya es el objeto User validado por la dependencia
    # FastAPI filtrará automáticamente los campos según el response_model User
    # (Asegúrate que User no exponga la contraseña hash si se usa como response_model)
    # Si User expone el hash, crea un DTO UserRead sin la contraseña.
    return current_user


# --- Endpoint Protegido: Ejemplo ---
@app.get("/items")
async def read_items(current_user: Annotated[User, Depends(get_current_user)]):
    """Endpoint de ejemplo protegido."""
    return [{"item_id": "Foo", "owner_id": current_user.id, "owner_name": current_user.name}]


# --- Endpoint para Feedback (Protegido o no, según decidas) ---
# Asumiendo que necesita autenticación para saber quién envía el feedback
@app.post("/feedback", status_code=status.HTTP_201_CREATED)
def add_feedback(
    feedback_data: FeedbackCreate, # Recibe los datos del feedback
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)] # Requiere autenticación
):
    """Crea una nueva entrada de feedback para el usuario autenticado."""
    # Asegurarse que el user_id en feedback_data coincide con el usuario autenticado
    # o simplemente usar el current_user.id
    if feedback_data.user_id != current_user.id:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes enviar feedback en nombre de otro usuario."
         )

    # Crear el feedback usando el user_id del usuario autenticado
    # (Podrías modificar FeedbackCreate para no requerir user_id y tomarlo del token)
    db_feedback = create_feedback(session=session, feedback=feedback_data)
    if db_feedback is None:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo guardar el feedback."
         )
    # Devolver el feedback creado (o un mensaje de éxito)
    return db_feedback