from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Modelo para actualizar el perfil de usuario.
# Los campos son opcionales para permitir actualizaciones parciales.
class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
