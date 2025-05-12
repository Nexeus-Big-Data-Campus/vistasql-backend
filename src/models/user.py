import uuid
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()), 
        primary_key=True,
        index=True,
    )
    name: str
    email: str = Field(index=True, unique=True)
    password: str
    