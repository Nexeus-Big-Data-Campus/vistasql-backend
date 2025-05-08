from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from .feedback import Feedback

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str
    
    feedbacks: List["Feedback"] = Relationship(back_populates=" user")