from fastapi import FastAPI
from src.db import engine
from sqlmodel import SQLModel
from src.crud import feedback_crud

app = FastAPI()
app.include_router(feedback_crud.router)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}

