import logging
from typing import Protocol
from fastapi import HTTPException
from passlib.context import CryptContext
from app.api.schema.pydantic import LoginSchema
from app.api.auth_repo import JWTRepo
from app.infrastructure.database.repositories.user import UsersRepository
from app.exceptions.custom_exceptions import InvalidPasswordException, UsernameNotFoundException

logger = logging.getLogger(__name__)

# Encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginUser:
    def __init__(self, user_repo: UsersRepository, token_repo: JWTRepo):
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def login(self, login: LoginSchema):
        _username = await self.user_repo.find_by_username(login.username)

        if _username is not None and pwd_context.verify(login.password, _username.password):
            logger.info(f"User {_username.username} logged in successfully")
            self.token_repo.data = {"username": _username.username}
            return self.token_repo.create_access_token()
        logger.warning(f"Failed login attempt for username: {login.username}")
        raise UsernameNotFoundException("Invalid credentials !")