from src.dto.login import LoginRequest
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.crud.user_crud import get_user_by_email
from src.security.security import verify_password, create_jwt_token


router = APIRouter()

@router.post("/login")
def login(datos: LoginRequest, db: Session = Depends(get_session)):
    usuario = get_user_by_email(db, datos.email)

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    if not verify_password(datos.password, usuario.password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")


    token = create_jwt_token(usuario)
    return {"access_token": token}
