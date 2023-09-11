from app.model.user import User
from app.core.db_config import db
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
        
    staticmethod
    async def get_user_by_username(username: str) -> User:
        async with db as session:
            query = select(User).where(User.username == username)
            result = await session.execute(query)
            user = result.scalars().first()
            return user
    
    @staticmethod
    async def update_user(user_id: int, updated_data: User) -> None:
        async with db as session:
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            user = result.scalars().first()
            user.username = updated_data.username
            user.email = updated_data.email
            query = sql_update(User).where(User.id == user_id).values(**user.dict()).execution_options(synchronize_session="fetch")
            await session.execute(query)
            await db.commit_rollback()
    
    @staticmethod
    async def delete_user(user_id: int) -> None:
        async with db as session:
            query = sql_delete(User).where(User.id == user_id)
            await session.execute(query)
            await db.commit_rollback()
