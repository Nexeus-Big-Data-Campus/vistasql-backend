from sqlmodel import SQLModel, create_engine
from passlib.context import CryptContext 
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)
# Encriptar contraseña
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")