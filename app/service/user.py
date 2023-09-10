import logging
from datetime import datetime

import bcrypt
from app.repository.user import UserRepository
from app.schema.user import LoginResponse, UserRegistrationInput, UserType
from app.model.user import User
from passlib.context import CryptContext
import app.utils.authentication as auth
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Custom Exception Classes
class AuthenticationError(Exception):
    pass

class UserAlreadyExistsError(Exception):
    pass

class UserNotFoundError(Exception):
    pass


class UserService:

    @staticmethod
    async def register_user(user_data: UserRegistrationInput) -> User:
        # Check if a user with the given email already exists.
        existing_user = await UserRepository.get_user_by_email(user_data.email)
        if existing_user:
            raise UserAlreadyExistsError("A user with this email already exists.")

        # Hash the password.
        hashed_password = auth.hash_password(user_data.password)

        # Create the User object.
        user = User(username=user_data.username, email=user_data.email, hashed_password=hashed_password)

        # Save the user to the database.
        await UserRepository.create_user(user)

        return UserType(id=user.id, email=user.email, username=user.username)
    
    @staticmethod
    async def authenticate_user(email: str, password: str) -> LoginResponse:
        user = await UserRepository.get_user_by_email(email)
        if not user:
            raise AuthenticationError("Invalid email or password.")
        
        if not auth.verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid email or password.")
        
        access_token = auth.create_access_token(data={"sub": user.email})
        return LoginResponse(access_token=access_token)

    
    @staticmethod
    async def fetch_all_users() -> list[User]:
        list_users = await UserRepository.get_all_users()
        return [UserType(id=user.id, email=user.email, username=user.username) for user in list_users]
    
    @staticmethod
    async def fetch_user_by_id(user_id: int) -> User:
        user = await UserRepository.get_user_by_id(user_id)
        return UserType(id=user.id, email=user.email, username=user.username)
    
    @staticmethod
    async def fetch_user_by_email(email: str) -> User:
        user = await UserRepository.get_user_by_email(email)
        return UserType(id=user.id, email=user.email, username=user.username)
