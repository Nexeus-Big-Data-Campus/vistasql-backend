from pydantic import BaseModel
from src.models.feedback import MessageType

class FeedbackCreate (BaseModel):
    user_id: int
    message_type: MessageType
    message : str