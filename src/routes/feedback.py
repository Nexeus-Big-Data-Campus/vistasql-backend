from typing import Annotated
from sqlmodel import Session
from src.crud import create_feedback
from src.db import get_session
from src.dto import FeedbackCreate
from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/")
def add_feedback(
    feedback: FeedbackCreate,
    session: Annotated[Session, Depends(get_session)],
):
    return create_feedback(session, feedback)