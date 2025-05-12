# src/user.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class Role(str, Enum):
    client = "client"
    admin = "admin"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str
    role: Role = Field(default=Role.client)  
    created_at: datetime = Field(default_factory=lambda: datetime.now(datetime.timezone.utc))  
    
class UserSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")  
    start_time: datetime = Field(default_factory=lambda: datetime.now(datetime.timezone.utc))
    end_time: Optional[datetime] = None
    duration: Optional[int] = None  
    
class UserAction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")  
    action: str  
    timestamp: datetime = Field(default_factory=lambda: datetime.now(datetime.timezone.utc))