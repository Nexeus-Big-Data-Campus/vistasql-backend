from fastapi import APIRouter, Depends
from sqlmodel import Session
from src.db import engine
from src.models.feedback import Feedback
from src.schemas.feedback import FeedbackCreate

router = APIRouter

@router.post("/feedback")
def create_feedback (feedback: FeedbackCreate, session: Session = Depends(engine)):
    db_feedback = Feedback(**feedback.model_dump())
    session.add(db_feedback)
    session.commit()
    session.refresh(db_feedback)
    return db_feedback

