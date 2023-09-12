from typing import Optional
import strawberry


@strawberry.type
class UserType:
    id: str
    username: str
    email: str

@strawberry.type
class LoginResponse:
    message: str
    token: str

@strawberry.input
class UserRegistrationInput:
    username: str
    email: str
    password: str

@strawberry.input
class UserUpdateInput:
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]