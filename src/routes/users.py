from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException
from src.crud import delete_user
from src.db import get_session

router = APIRouter()

@router.delete("/{user_id}")
def remove_user(user_id: str, session: Annotated[Session, Depends(get_session)]):
    success = delete_user(session, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}