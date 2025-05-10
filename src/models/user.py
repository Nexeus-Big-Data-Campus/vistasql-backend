from sqlmodel import SQLModel, Field
from typing import Optional
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# recuperamos la clave secreta del entorno, le he añadido una validación y un casteo a str para evitar el error 500
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_SECRET_KEY = str(JWT_SECRET_KEY)

if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY no está definido en las variables de entorno")
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str
    

def create_token(email, name):
    '''función para crear un token JWT'''
    token_data = {    
        "email": email,
        "name": name,
        "exp": datetime.utcnow() + timedelta(hours=24)  # Token válido por 24 horas
    }
    token = jwt.encode(token_data, JWT_SECRET_KEY, algorithm="HS256") 
    return token