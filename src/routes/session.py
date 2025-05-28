from datetime import datetime
from typing import Annotated
from sqlmodel import Session
from src.db.db import get_session
from src.models import UserSession
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

@router.put("/sign-out")
def logout_user(
    session_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    user_session = session.query(UserSession).filter(
        UserSession.id == session_id,
        UserSession.end_time == None
    ).first()

    if user_session:
        user_session.end_time = datetime.now(datetime.timezone.utc)
        session.commit()
        return {"message": "Session closed successfully"}
    else:
        raise HTTPException(
            status_code=404,
            detail="Session not found or already closed"
        )
    
@router.get("/{user_id}")
def get_user_sessions(user_id: int, session: Annotated[Session, Depends(get_session)]):
    sessions = session.query(UserSession).filter(UserSession.user_id == user_id).all()
    return sessions