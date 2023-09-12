from typing import Generic, Optional, TypeVar
import strawberry

T = TypeVar("T")

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

@strawberry.input
class ForgotPasswordSchema:
    email: str
    new_password: str


@strawberry.type
class ResponseSchemaGql(Generic[T]):
    detail: str
    result: Optional[T] = None

@strawberry.type
class UserType:
    id: str
    username: str
    email: str

@strawberry.type
class LoginResponse:
    message: str
    token: str