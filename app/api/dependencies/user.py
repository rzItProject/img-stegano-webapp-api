from fastapi import Depends
from jose import JWTError, jwt
from app.api.auth_repo import JWTRepo

from app.api.dependencies.token import get_current_token
from app.exceptions.custom_exceptions import (
    InvalidTokenException,
    TokenMissingException,
    UserNotFoundException,
)
from app.infrastructure.database.orm_models.users import Users
from app.infrastructure.database.repositories.user import UsersRepository


async def get_current_user(token: str = Depends(get_current_token)) -> Users:
    if not token:
        raise TokenMissingException()
    try:
        jwtRepo = JWTRepo(token=token)
        payload = jwtRepo.decode_token()
    except JWTError:
        raise InvalidTokenException()

    username: str = payload.get("username")
    if username is None:
        raise InvalidTokenException

    user = await UsersRepository.find_by_username(username)
    if not user:
        raise UserNotFoundException()

    return user
