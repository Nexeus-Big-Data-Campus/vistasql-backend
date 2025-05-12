from sqlmodel import Session, select
from typing import Optional
from src.models import User
from src.dto import UserCreate
from src.security import get_password_hash


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

<<<<<<< HEAD:src/crud/crud.py
# se agrega la nueva funcion
def get_user_by_id(session: Session, user_id: str) -> Optional[User]:
    """Se obtiene un usario por su ID"""
    statement= select(User).where(User.id == user_id)
    return session.exec(statement).first()
    

def create_user(session: Session, user_in: UserCreate) -> User:
=======
def create_user(session: Session, user_in: UserCreate) -> Optional[User]:
>>>>>>> develop:src/crud/user_crud.py
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
