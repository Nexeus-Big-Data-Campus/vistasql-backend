from sqlmodel import Session, select
from typing import Optional
from src.models import User
from src.dto import UserCreate
from src.security import get_password_hash
from fastapi import Depends, HTTPException,status
from src.db.db import get_session
from src.models import User
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.security.security import decode_jwt_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/sign-in")  



def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def get_user_by_id(session: Session, user_id: str) -> Optional[User]:
    statement = select(User).where(User.id == user_id)
    return session.exec(statement).first()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_session)
):
    try:
        payload = decode_jwt_token(token)
        user_id: str = payload.get("id")  # <- Asegúrate de que el token incluya el campo "id"
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        user = get_user_by_id(db, user_id=user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar el token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def create_user(session: Session, user_in: UserCreate) -> Optional[User]:
    existing_user = get_user_by_email(session, user_in.email)
    if existing_user:
        return None
            
    hashed_password = get_password_hash(user_in.password)
    from src.models.user import Role
    db_user = User(
        email=user_in.email, 
        password=hashed_password, 
        name=user_in.name,
        role=Role.client)
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

def delete_user(session: Session, user_id: str) -> bool:
    user = session.get(User, user_id)    

    if user:
        session.delete(user)
        session.commit()
        return True
    return False