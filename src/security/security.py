import os
import jwt
from datetime import datetime, timedelta
# se Añade HTTPAutoizationCrede...
from typing import Optional, Annotated # Se añade Annotated
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status # Se añade HTTTPException, status
#from fastapi.security import OAuth2PasswordBearer # se comenta para activar la barra de token

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session #se añade Session
from src.db import engine #necesario para get_session
from src.models import User
#from src.crud import get_user_by_id # 



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_jwt_token(data: dict):
    to_encode = data.copy()
    expiration_date = datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
    to_encode.update({"exp": expiration_date})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_jwt_token(token: str):
<<<<<<< HEAD
    try:
        # se usa jwt.PyJWTError que es la excepcion base de PyJWT
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    # Captura excepciones especificas
    except jwt.ExpiredSignatureError:
        # se podria manejar la expiracion de forma especifica
        return None
    except jwt.PyJWTError as e: #se captura cualquier error de PyJWT
        #print(f'JWT Error:{e}')
        return None
""" se define el esquema de autenticacion
    tokenUrl idealmente apunta al endpoint de login/token (ejemplo "sign-in")
    esto es usado principalmente para la documentacion de Sqgger UI
"""
# Se reemplaza outh2_sheme por barear_sheme usando HTTPBearer()
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="sign-in")
bearer_scheme = HTTPBearer()

#Funcion para obtener la sesion de BD(ya esta en main se trae aca para la dependencia)
#o se podria importarla directamente desde main si se prefiere duplicarla
def get_session():
    with Session(engine) as session:
        yield session

# la dependencia de autenticacion
async def get_current_user(
    #token: Annotated[str, Depends(oauth2_scheme)],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    session: Annotated[Session, Depends(get_session)] # se inuecta sesion de BD
) -> "User":
    credential_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        #headers={"WWW-Authenticate": "Bearer"},
    )
    # se extra token de las credenciales
    token= credentials.credentials

    payload = decode_jwt_token(token)
    if payload is None:
        raise credential_exception
    
    user_id: Optional[str] = payload.get("id")# asumiendo que se guarda id en el payload
    if user_id is None:
        raise credential_exception
    from src.crud import get_user_by_id

    # Obtener el usuario de la base de datos
    user = get_user_by_id(session=session, user_id=user_id)
    if user is None:
        # Aunque el token sea valido, el usuario podria haber sido eliminado
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return user
=======
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    return payload
>>>>>>> develop
