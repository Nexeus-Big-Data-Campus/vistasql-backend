import os
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated 
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session 

#Importacion de proyecto
from src.db import engine #necesario para get_session
from src.models import User
from src.crud import get_user_by_id


# Configuracion de Passlib para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuracion de JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24

# Esquema de autenticacion Bearer
bearer_scheme = HTTPBearer()

def create_jwt_token(data: dict):
    to_encode = data.copy()
    expiration_date = datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
    to_encode.update({"exp": expiration_date})
    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRER_KEY no esta configurada en las variables")
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def decode_jwt_token(token: str):

    try:
        if not JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY no esta configurada para decodificar")
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    # Captura excepciones especificas
    except jwt.ExpiredSignatureError:
        # se podria manejar la expiracion de forma especifica
        return None
    except jwt.PyJWTError as e: #se captura cualquier error de PyJWT
        #print(f'JWT Error:{e}')
        return None
    except Exception as e:
        print(f"Error inespeado al decodificar token{e}")
        return None

def get_session():
    with Session(engine) as session:
        yield session

# la dependencia de autenticacion
async def get_current_user(
    #token: Annotated[str, Depends(oauth2_scheme)]
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    session: Annotated[Session, Depends(get_session)] # se inuecta sesion de BD
) -> User:
    credential_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # se extra token de las credenciales
    token= credentials.credentials

    payload = decode_jwt_token(token)
    if payload is None:
        raise credential_exception
    
    user_id: Optional[str] = payload.get("id")# asumiendo que se guarda id en el payload
    if user_id is None:
        raise credential_exception
    

    # Obtener el usuario de la base de datos
    user = get_user_by_id(session=session, user_id=user_id)
    if user is None:
        # Aunque el token sea valido, el usuario podria haber sido eliminado
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    

    #payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    return user

