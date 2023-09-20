from sqlalchemy import update as sql_update
from sqlalchemy.future import select
from app.infrastructure.database.orm_models.users import Users
from app.infrastructure.database.repositories.base_repo_crud import BaseCrud


from app.infrastructure.database.session import db


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