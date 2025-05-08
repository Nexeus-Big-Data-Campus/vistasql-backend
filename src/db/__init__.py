from .db import engine
from sqlmodel import SQLModel

def init_db(engine):
    SQLModel.metadata.create_all(engine)