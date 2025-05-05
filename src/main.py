from fastapi import FastAPI
from src.db import engine
from sqlmodel import SQLModel
from src.models import User

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}