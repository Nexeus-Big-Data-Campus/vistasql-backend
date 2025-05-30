import uuid
from sqlmodel import SQLModel, Field
from typing import Optional
from src.security import create_jwt_token

class User(SQLModel, table=True):
    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()), 
        primary_key=True,
        index=True,
    )
    
    name: str
    email: str = Field(index=True, unique=True)
    password: str
    

    def get_jwt_token(self):
        return create_jwt_token({
            'id': self.id,
            'name': self.name,
            'email': self.email,
        })
        
    