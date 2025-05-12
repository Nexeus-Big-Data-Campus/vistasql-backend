from fastapi import APIRouter
from sqlmodel import Session
from ..models.feedback import Feedback
from src.dto.feedback import FeedbackCreate

router = APIRouter()

def create_feedback(
    session: Session,
    feedback: FeedbackCreate,
):
    db_feedback = Feedback(
        user_id=feedback.user_id,
        message_type=feedback.message_type,
        message=feedback.message,
    )
    session.add(db_feedback)
    session.commit()
    session.refresh(db_feedback)
    return db_feedback