from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import BaseModel # Para el modelo de entrada


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: Optional[str] = None

class User(UserBase, table=True):
    """Modelo de usuario para la base de datos."""
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str # contraseña hasheada se almacena aca

class UserCreate(UserBase):
    """Modelo para la creacion de un nuevo usuario(entrada del endpoint)."""
    password: str # se recibe la contraseña plana

class UserResponse(UserBase):
    """Modelo para la respuesta del endpoint de usuario(sin contraseña hacheada)"""
    id: int
    # se puede añadir el token JWT aca si queremos devolver junto con los datos del usuario
    # toke: str

class Token(BaseModel):
    """Modelo para la respuesta del token JWT."""
    access_token: str
    token_type: str = "bearer"
    # se puede añadir la informacion del usuario si quieres que venga con el token
    # user_id: int
    # user_email: str

"""Nota: se añade UserBase para compartir campos comunes y UserResponse para usarlo si en el futuro se necesita devolver 
informacion del usuario sin la contrasela hasheada. El token modelo es para estrucurar la respuiesta del endpoint de registro"""