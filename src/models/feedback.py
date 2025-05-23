import uuid
from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum

class MessageType (str, Enum):
    bug = "bug"
    feedback = "feedback"

class Feedback(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    message_type: MessageType
    message: str