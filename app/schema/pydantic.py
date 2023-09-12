import logging
import re
from typing import Optional
from pydantic import BaseModel, validator
from fastapi import HTTPException
from typing import TypeVar, Optional
from app.model.person import Sex

T = TypeVar('T')

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


class RegisterSchema(BaseModel):

    username: str
    email: str
    name: str
    password: str
    birth: str
    sex: Sex
    profile: str = "base64"

    # Sex validation
    @validator("sex")
    def sex_validation(cls, v):
        if hasattr(Sex, v) is False:
            raise HTTPException(status_code=400, detail="Invalid input sex")
        return v


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
