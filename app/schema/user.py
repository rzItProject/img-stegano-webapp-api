from typing import Optional
import strawberry

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
