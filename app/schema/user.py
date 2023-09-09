import strawberry
from typing import Optional
from pydantic import BaseModel

class LoginInput(BaseModel):
    email: str
    password: str

# user

@strawberry.type
class UserType:
    id: int
    username: str
    email: str

@strawberry.type
class LoginResponse:
    access_token: str


@strawberry.input
class UserRegistrationInput:
    username: str
    email: str
    password: str

@strawberry.input
class UserLoginInput:
    email: str
    password: str

@strawberry.input
class UserUpdateInput:
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
