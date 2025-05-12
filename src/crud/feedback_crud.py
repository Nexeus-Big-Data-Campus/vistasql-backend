from fastapi import APIRouter, Depends
from sqlmodel import Session
from src.db.db import get_session
from ..models.feedback import Feedback
from src.dto.feedback import FeedbackCreate

router = APIRouter()

@router.post("/feedback")
def create_feedback(
    feedback: FeedbackCreate,
    session: Session = Depends(get_session)
):
    db_feedback = Feedback(**feedback.model_dump())
    session.add(db_feedback)
    session.commit()
    session.refresh(db_feedback)
    return db_feedback