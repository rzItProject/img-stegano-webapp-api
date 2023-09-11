from typing import Optional
from pydantic import BaseModel

class UserType(BaseModel):
    id: int
    username: str
    email: str

class CreateUserInput(BaseModel):
    username: str
    password: str
    email: str

class LoginUserInput(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    user_id: Optional[str] = None
