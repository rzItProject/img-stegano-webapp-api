import base64
from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException

from passlib.context import CryptContext

from app.api.schema.pydantic import LoginSchema, RegisterSchema
from app.api.schema.strawberry import ForgotPasswordSchema

from app.infrastructure.database.orm_models.person import Person
from app.infrastructure.database.orm_models.role import Role
from app.infrastructure.database.orm_models.user_role import UsersRole
from app.infrastructure.database.orm_models.users import Users

from app.api.auth_repo import JWTRepo
from app.infrastructure.database.repositories.person import PersonRepository
from app.infrastructure.database.repositories.role import RoleRepository
from app.infrastructure.database.repositories.user import UsersRepository
from app.infrastructure.database.repositories.user_role import UsersRoleRepository


# Encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



class AuthService:

    @staticmethod
    async def forgot_password_service(forgot_password: ForgotPasswordSchema):
        _email = await UsersRepository.find_by_email(forgot_password.email)
        if _email is None:
            raise HTTPException(status_code=404, detail="Email not found !")
        await UsersRepository.update_password(forgot_password.email, pwd_context.hash(forgot_password.new_password))
        


        