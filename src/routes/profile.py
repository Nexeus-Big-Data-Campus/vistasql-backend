from fastapi import APIRouter, Depends, Header
from sqlmodel import Session
from src.db.db import get_session
from src.security.security import get_user_from_token
from src.models.user import User

router = APIRouter()


@router.get("/profile")
def get_profile(
    token: str = Header(..., alias="Authorization"),
    session: Session = Depends(get_session)
):
    user = get_user_from_token(token, session)
    return {
        "id": user.id,
        "email": user.email,
        "nombre": user.nombre,
        "apellido": user.apellido
    }
