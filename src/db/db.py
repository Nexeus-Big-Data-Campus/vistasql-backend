from sqlmodel import create_engine, Session
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv(dotenv_path="./.env")

# Generar DATABASE_URL si no está definida
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("DATABASE_URL no se encuentra, generando desde las variables...")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    dbname = os.getenv("POSTGRES_DB")
    
    DATABASE_URL = f"postgresql://{user}:{password}@localhost/{dbname}"
    print(f"DATABASE_URL generada correctamente: {DATABASE_URL}")

# Verificación final
if not DATABASE_URL:
    raise ValueError("No se pudo generar la URL de la base de datos.")

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
