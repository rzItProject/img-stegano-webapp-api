import logging
from typing import Optional
from pydantic import BaseModel, EmailStr, constr
from fastapi import HTTPException
from typing import TypeVar, Optional
from app.api.schema.validators import RegisterValidators
from app.exceptions.custom_exceptions import InvalidPasswordException

from app.infrastructure.database.orm_models.person import Gender


T = TypeVar("T")

# get root logger
logger = logging.getLogger(__name__)


class UserType(BaseModel):
    id: str
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


class RegisterSchema(RegisterValidators):
    # les autres champs sont dans le validator (username etc)
    email: EmailStr  # Permet de vérifier si un email est valide
    name: str
    profile_picture: str = "base64"


class LoginSchema(BaseModel):
    username: str
    password: str


class DetailSchema(BaseModel):
    status: str
    message: str
    result: Optional[T] = None


class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None


class ImageResponseModel(BaseModel):
    id: str
    image_link: str
    image_data: str

class ImageUrlResponseModel(BaseModel):
    url: str

