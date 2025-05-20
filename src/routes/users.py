from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel import Session
from src.crud import delete_user
from src.db import get_session
from src.dto.user import UserUpdate
from src.models import User  
from src.security.security import get_current_user  

router = APIRouter()

@router.get("/me")
def get_current_user_data(
    current_user: User = Depends(get_current_user)
):
    return current_user

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