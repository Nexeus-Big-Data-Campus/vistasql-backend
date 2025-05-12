import os
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session
from typing import Annotated

from src.db import engine
<<<<<<< HEAD
from src.crud import create_user, get_user_by_email
from src.dto import UserCreate
#from datetime import timedelta
from src.security import get_current_user
from src.models import User #Se importa User
=======
from src.crud import create_user, create_feedback
from src.dto import UserCreate, FeedbackCreate
>>>>>>> develop

ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
dosc_url = "/docs" if ENVIRONMENT != "prod" else None #Corregido "dosc_url"
app = FastAPI(docs_url=dosc_url, redoc_url=None)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# se mueve get.session aqui si no se importa desde security
def get_session():
    with Session(engine) as session:
        yield session

# Endpoint publico (login/registro)
@app.post("/sign-in")
def register_user(user: UserCreate, session: Annotated[Session, Depends(get_session)]):
    
    db_user = get_user_by_email(session, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El correo ya existe")
    
    new_user = create_user(session, user)
<<<<<<< HEAD
    #No se necesita verificar si new_user es None porque create_user ya lo hace
    
    token = new_user.get_jtw_token()
    return {"access_token": token, "token_type": "bearer"}

# Endpoint protegido
@app.get("/users/me")
#Añade la dependencia aqui. FastApi ekecutara get_curren_user primero
#si tiene exito, el objeto User estara en current_user
#si falla (token invalido, etc) get_current_user lanzara HTTPException
#y la ajecucion no llegara al cuerpo de esta funcion
async def read_users_me(current_user: Annotated["User", Depends(get_current_user)]):
    # ahora tienes acceso al usuario autentificado a traves de current_user
    return {"user_id": current_user.id, "email": current_user.email, "name": current_user.name}

# otro enpoint protegido
app.get("/items")
async def read_items(current_user: Annotated[User, Depends(get_current_user)]):
    #solo usuarios autentificados pueden acceder aqui
    #Puedes usar current_user.id si necesita filtrar items por usuario
    return [{"item_id": "Foo", "owner": current_user.name}]
=======
    if new_user is None:
        raise HTTPException(status_code=400, detail="Email already exsists")

    token = new_user.get_jwt_token()
    return {"access_token": token, "token_type": "bearer"}

@app.post("/feedback")
def add_feedback(
    feedback: FeedbackCreate,
    session: Annotated[Session, Depends(get_session)],
):
    return create_feedback(session, feedback)
>>>>>>> develop
