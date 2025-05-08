from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está definida en el archivo .env")

engine = create_engine(DATABASE_URL, echo=True)