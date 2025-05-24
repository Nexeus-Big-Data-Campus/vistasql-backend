import uuid
from sqlmodel import SQLModel, Field
from typing import Optional
from src.security import create_jwt_token, verify_password
from datetime import datetime, timezone
from enum import Enum

class Role(str, Enum):
    client = "client"
    admin = "admin"

class User(SQLModel, table=True):
    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()), 
        primary_key=True,
        index=True,
    )
    name: str
    email: str = Field(index=True, unique=True)
    password: str
    role: Role = Field(default=Role.client)  
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    def get_jwt_token(self):
        return create_jwt_token({
            'id': self.id,
            'name': self.name,
            'email': self.email,
        })
    
    def verify_password(self, password: str) -> bool:
        return verify_password(password, self.password)
        
class UserSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")  
    start_time: datetime = Field(default_factory=lambda: datetime.now(datetime.timezone.utc))
    end_time: Optional[datetime] = None