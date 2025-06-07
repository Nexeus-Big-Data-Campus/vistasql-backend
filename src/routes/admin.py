from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from src.db import get_session
from src.middleware.auth_middleware import admin_required
from src.models import User
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/user-stats", dependencies=[Depends(admin_required)])
def user_stats(session: Session = Depends(get_session)):
    total = session.exec(select(func.count()).select_from(User)).one()
    last_month = datetime.now() - timedelta(days=30)
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