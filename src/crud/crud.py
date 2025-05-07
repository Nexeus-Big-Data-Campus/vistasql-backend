from sqlmodel import Session, select
from typing import Optional

from src.models.user import User, UserCreate # se importa los modelos user y Usercreate
from src.security import get_password_hash # se importa la funsion para hashear la contraseña

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """Busca un usuario por email en la base de datos."""
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def create_user(session: Session, user_in: UserCreate) -> User:
    """Crea un nuevo usuario en la bnase de datos."""
    hashed_password = get_password_hash(user_in.password)
    db_user = User(email=user_in.email, hashed_password=hashed_password, name=user_in.name ) # se crea la instancia del modelo user con la contraseña hasheada
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
