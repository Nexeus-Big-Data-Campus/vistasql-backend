from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from src.db import get_session
from src.models import User, UserSession
from datetime import datetime, timedelta
from src.routes.auth import get_current_user

router = APIRouter()

def admin_required(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return user

@router.get("/user-stats", dependencies=[Depends(admin_required)])
def user_stats(session: Session = Depends(get_session)):
    total = session.exec(select(func.count()).select_from(User)).one()
    last_month = datetime.now()
    last_month = last_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_month_count = session.exec(
        select(func.count()).select_from(User).where(User.created_at >= last_month)
    ).one()
    return {"total_users": total, "last_month": last_month_count}

@router.get("/user-registrations", dependencies=[Depends(admin_required)])
def user_registrations(session: Session = Depends(get_session)):
    results = session.exec(
        select(func.date(User.created_at), func.count())
        .group_by(func.date(User.created_at))
        .order_by(func.date(User.created_at))
    ).all()
    return [{"date": str(date), "count": count} for date, count in results]

@router.get("/average-session-duration", dependencies=[Depends(admin_required)])
def average_session_duration(session: Session = Depends(get_session)):
    sessions = session.exec(
        select(UserSession).where(UserSession.end_time.is_not(None))
    ).all()
    if not sessions:
        return {"average_duration": "00:00:00"}

    total_seconds = sum(
        (s.end_time - s.start_time).total_seconds() for s in sessions
    )
    avg_seconds = int(total_seconds // len(sessions))
    hours = avg_seconds // 3600
    minutes = (avg_seconds % 3600) // 60
    seconds = avg_seconds % 60
    avg_duration_str = f"{hours:02}:{minutes:02}:{seconds:02}"

    return {"average_duration": avg_duration_str}

