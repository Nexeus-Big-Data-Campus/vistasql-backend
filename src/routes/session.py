from datetime import datetime
from typing import Annotated
from sqlmodel import Session
from src.db.db import get_session
from src.models import UserSession
from fastapi import APIRouter, Depends, HTTPException
from src.crud.user_crud import get_current_user
from datetime import datetime
from typing import Annotated
from fastapi import Depends, HTTPException,status, APIRouter
from src.db.db import get_session
from src.dto.user import UserProfile


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

#Ver todas las sesiones del usuario    
@router.get("/{user_id}")
def get_user_sessions(
    email: str,
    session: Annotated[Session, Depends(get_session)],
    current_user=Depends(get_current_user)
):

    if current_user.email != email:
                raise HTTPException(status_code=403, detail="No tienes permisos para acceder a esta información.")

    sessions = session.query(UserSession).filter(UserSession.user_id == current_user.id).all()
    return sessions

#Ver todas las sesiones públicas
@router.get("/users/{user_id}",response_model=UserProfile)
def get_user_profile(user_id: str, current_user=Depends(get_current_user)):
    from src.crud.user_crud import get_user_by_id

    user = get_user_by_id(user_id)
    status_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Las credenciales introducidas no se corresponden con las suyas.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if user is None:
        raise status_exception
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Las credenciales introducidas no se corresponden con las suyas.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user = UserProfile(id=user.id,email=user.email,name=user.name,disabled=False,role="client",created_at=datetime.now())

    if user.email != current_user.email:
        raise credentials_exception
    




