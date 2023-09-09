import logging
import bcrypt
from datetime import datetime
from app.repository.user import UserRepository
from app.schema.user import UserRegistrationInput, UserType
from app.model.user import User

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
        hashed_password = UserService._hash_password(user_data.password)

        # Create the User object.
        user = User(username=user_data.username, email=user_data.email, hashed_password=hashed_password)

        # Save the user to the database.
        await UserRepository.create_user(user)

        return UserType(id=user.id, email=user.email, username=user.username)
    
    @staticmethod
    async def fetch_all_users() -> list[User]:
        list_users = await UserRepository.get_all_users()
        return [UserType(id=user.id, email=user.email, username=user.username) for user in list_users]
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """Hashes a password."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')