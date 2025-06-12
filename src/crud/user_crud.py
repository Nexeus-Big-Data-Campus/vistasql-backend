from sqlmodel import Session, select
from typing import Optional
from src.models import User
from src.dto import UserCreate
from src.security import get_password_hash
from fastapi import HTTPException

def verify_password(password):
    if len(password) < 8 :
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 8 caracteres")
    
def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def create_user(session: Session, user_in: UserCreate) -> Optional[User]:
    verify_password(user_in.password)
    existing_user = get_user_by_email(session, user_in.email)
    if existing_user:
        return None
            
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email, 
        password=hashed_password, 
        name=user_in.name)
    
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