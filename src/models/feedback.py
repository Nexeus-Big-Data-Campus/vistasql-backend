from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum

class MessageType (str, Enum):
    bug = "bug"
    feedback = "feedback"

class Feedback(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    message_type: MessageType
    message: str
    