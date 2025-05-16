
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.crud import get_user_by_email
from src.main import get_session
from src.models import User
from src.security import verify_password, create_jwt_token


app = FastAPI()

# Recibe los datos y verifica que son correctos
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = get_user_by_email(session, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Email o contraseña incorrectos")

    if user.disabled:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    
    # Crea un JWT con los datos de usuario
    access_token = create_jwt_token({"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}