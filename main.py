from fastapi import FastAPI
from src.db import engine
from sqlmodel import SQLModel
from src.models import User

app = FastAPI()

#modelo de entrada de datos

class LoginRequest(SQLModel):
    email: str 
    password: str

#usuarios de ejemplo 

fake_users_db = {
    "usuario@example.com": {
        "email": "usuario@example.com",
        "password": "123456"
    }
}

@app.post("/login")
def login(data: LoginRequest):
    user = fake_users_db.get(data.email)
    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Credenciales invalidas")
    return {"message": "Login exitoso", "user": data.email}


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}