from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from typing import Annotated
from sqlmodel import Session
from src.crud import create_feedback
from crud.user_crud import delete_user
from src.db import get_session
from src.dto import FeedbackCreate
from src.dto.user import UserUpdate
from src.models import User  
from src.security.security import get_current_user
from src.routes.auth import get_user_from_token
from fastapi.security import OAuth2PasswordBearer
from src.security.security import decode_jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/users")

router = APIRouter()

@router.get("/login")
@router.get("/register")
def redirect_authenticated_user(
    current_user: dict = Depends(get_current_user),
):
    """
    Si el usuario ya está autenticado, redirige a /editor
    """
    if current_user:
        return RedirectResponse(url="/editor", status_code=303)

    # Si por alguna razón no entra en el if (no debería pasar), devolver algo
    return {"message": "Este endpoint solo se muestra si NO estás autenticado"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_jwt_token(token)
        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="No autorizado")

@router.put("/{user_id}")
def update_user(
    user_id: str,
    user_data: UserUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    # Validar que el usuario es el propietario de la cuenta
    if current_user["id"] != user_id:
        raise HTTPException(403, "No tienes permiso para realizar esta acción")
    
    # Actualizar datos en la base de datos
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "Usuario no encontrado")
    
    # Aplicar cambios (ejemplo simplificado)
    user.name = user_data.name or user.name
    user.email = user_data.email or user.email
    session.commit()
    return {"message": "Usuario actualizado"}

@router.delete("/{user_id}")
def remove_user(
    user_id: str,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    if current_user["id"] != user_id:
        raise HTTPException(403, "No tienes permiso para eliminar esta cuenta")
    
    success = delete_user(session, user_id)
    if not success:
        raise HTTPException(404, "Usuario no encontrado")
    return {"message": "Cuenta eliminada exitosamente"}

@router.get("/{id_usuario}")
def get_user_profile(
    id_usuario: str,  
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Devuelve los datos del usuario desde la base de datos,
    y verifica que el usuario autenticado sea el mismo que el solicitado.
    """
    if current_user["id"] != id_usuario:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para ver estos datos"
        )
    user_db = session.get(User, id_usuario)

    if not user_db:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    return {
        "id": user_db.id,
        "email": user_db.email,
        "nombre": user_db.name,
        "role": user_db.role
    }
        
@router.post("/")
def add_feedback(
    feedback: FeedbackCreate,
    session: Annotated[Session, Depends(get_session)],
):
    return create_feedback(session, feedback)