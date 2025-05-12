import uuid
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from src.security import create_jwt_token

if TYPE_CHECKING:
    from .feedback import Feedback

class User(SQLModel, table=True):
    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()), 
        primary_key=True,
        index=True,
    )
    
    name: str
    email: str = Field(index=True, unique=True)
    password: str
    
    feedbacks: List["Feedback"] = Relationship(back_populates="user")

    def get_jwt_token(self):
        return create_jwt_token({
            'id': self.id,
            'name': self.name,
            'email': self.email,
        })
        
    