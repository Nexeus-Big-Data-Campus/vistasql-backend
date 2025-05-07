import os
from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext
from jose import JWTError, jwt

# Configuración de hashing de contraseñas
# Usamos schemes=["bcrypt"] que requiere librerías del sistema operativo
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de JWT
SECRET_KEY = os.getenv("SECRET_KEY", "tu_super_clave_secreta") # ¡Cambia esto en producción y usa variables de entorno!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña plana coincide con una contraseña hasheada."""
    # Agregamos una verificación para evitar errores si hashed_password es None inesperadamente
    if hashed_password is None:
        return False
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashea una contraseña.
    Lanza un error si el hashing falla y devuelve None.
    """
    hashed_password = pwd_context.hash(password)

    # --- Verificación añadida ---
    if hashed_password is None:
        # Si el hashing devuelve None, algo salió mal.
        # Lanzamos un error explícito para obtener un traceback detallado.
        raise RuntimeError("Password hashing failed. Check passlib and system dependencies.")
    # ---------------------------

    return hashed_password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crea un token de acceso JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """Decodifica un token de acceso JWT."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
