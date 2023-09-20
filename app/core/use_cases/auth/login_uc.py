from typing import Protocol
from fastapi import HTTPException
from passlib.context import CryptContext
from app.api.schema.pydantic import LoginSchema
from app.infrastructure.database.repositories.auth_repo import JWTRepo
from app.infrastructure.database.repositories.user import UsersRepository
from app.exceptions.custom_exceptions import InvalidPasswordException, UsernameNotFoundException

# Encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginUser:
    def __init__(self, user_repo: UsersRepository, token_service: JWTRepo):
        self.user_repo = user_repo
        self.token_service = token_service

    async def login(self, login: LoginSchema):
        _username = await self.user_repo.find_by_username(login.username)

        if _username is not None:
            if not pwd_context.verify(login.password, _username.password):
                raise InvalidPasswordException("Invalid Password or Username !")
            return self.token_service.create_access_token(data={"username": _username.username})
        raise UsernameNotFoundException("Invalid Password or Username !")