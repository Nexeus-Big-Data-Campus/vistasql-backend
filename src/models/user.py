from sqlmodel import SQLModel, Field
from typing import Optional
import jwt
from src.main import JWT_SECRET_KEY
from datetime import datetime, timedelta
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