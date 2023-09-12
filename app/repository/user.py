from sqlalchemy import update as sql_update
from sqlalchemy.future import select


from app.core.db_config import db
from app.model.users import Users
from app.repository.base_repo_crud import BaseCrud


class UsersRepository(BaseCrud):
    model = Users

    @staticmethod
    async def find_by_username(username: str):
        async with db as session:
            query = select(Users).where(Users.username == username)
            return (await session.execute(query)).scalar_one_or_none()

    @staticmethod
    async def find_by_email(email: str):
        async with db as session:
            query = select(Users).where(Users.email == email)
            return (await session.execute(query)).scalar_one_or_none()

    @staticmethod
    async def update_password(email: str, password: str):
        async with db as session:
            query = sql_update(Users).where(Users.email == email).values(
                password=password).execution_options(synchronize_session="fetch")
            await session.execute(query)
            await db.commit_rollback()

    @staticmethod
    async def update_username(email: str, password: str):
        async with db as session:
            query = sql_update(Users).where(Users.email == email).values(
                password=password).execution_options(synchronize_session="fetch")
            await session.execute(query)
            await db.commit_rollback()

    # TODO: UPDATE EMAIL, USERNAME