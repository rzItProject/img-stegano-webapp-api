from app.model.user import User
from app.database.config import db
from sqlalchemy.sql import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update as sql_update, delete as sql_delete


# Custom Exception Classes
class UserNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class UserRepository:
    @staticmethod
    async def create_user(user_data: User) -> None:
        """Creates a new user in the database."""
        async with db as session:
            async with session.begin():

                
                try:
                    session.add(user_data)
                    await db.commit_rollback()
                except IntegrityError:
                    raise UserAlreadyExistsError(
                        "A user with the provided email or username already exists."
                    )

    @staticmethod
    async def get_all_users(offset: int = 0, limit: int = 10) -> list[User]:
        """Retrieves all users from the database with limit."""
        async with db as session:
            stmt = select(User).offset(offset).limit(limit)
            result = await session.execute(stmt)
            return result.scalars().all()
        
    @staticmethod
    async def get_user_by_id(user_id: int) -> User:
        """Retrieves a user from the database by their ID."""
        async with db as session:
            stmt = select(User).where(User.id == user_id)
            result = await session.execute(stmt)
            user = result.scalars().first()
            return user
        
    @staticmethod
    async def get_user_by_email(email: str) -> User:
        """Retrieves a user from the database by their ID."""
        async with db as session:
            stmt = select(User).where(User.email == email)
            result = await session.execute(stmt)
            user = result.scalars().first()
            return user
