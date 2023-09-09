from datetime import datetime

from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "note"
    
    id: int = Field(default=None, primary_key=True, index=True)
    username: str = Field(index=True, unique=True, min_length=3, max_length=50)
    email: str = Field(index=True, unique=True, regex=r"[^@]+@[^@]+\.[^@]+")
    hashed_password: str
    is_active: bool = Field(default=True)
    full_name: Optional[str] = Field(max_length=100)
    #created_at: datetime = Field(default=datetime.utcnow)
    #updated_at: datetime = Field(default=datetime.utcnow)
