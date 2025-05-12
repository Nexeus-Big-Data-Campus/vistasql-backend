from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from enum import Enum
from src.models.user import User

class MessageType (str, Enum):
    bug = "bug"
    feedback = "feedback"

class Feedback(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    message_type: MessageType
    message: str
    
    user: Optional[User] = Relationship(back_populates ="feedbacks")
    