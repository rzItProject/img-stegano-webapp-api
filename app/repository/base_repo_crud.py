
from typing import Generic, TypeVar
from sqlalchemy import update as sql_update, delete as sql_delete
from sqlalchemy.future import select
from app.core.db_config import db

T = TypeVar('T')


class BaseCrud:
    model = Generic[T]

    @classmethod
    async def create(cls, **kwargs):
        model = cls.model(**kwargs)
        async with db as session:
            async with session.begin():
                session.add(model)
                await db.commit_rollback()
        return model

    @classmethod
    async def get_all(cls):
        async with db as session:
            query = select(cls.model)
            return(await session.execute(query)).scalars().all()

    @classmethod
    async def get_by_id(cls, model_id: str):
        async with db as session:
            query = select(cls.model).where(cls.model.id == model_id)
            return (await session.execute(query)).scalar_one_or_none()

    @classmethod
    async def update(cls, model_id: str, **kwargs):
        async with db as session:
            query = sql_update(cls.model).where(cls.model.id == model_id).values(
                **kwargs).execution_options(synchronize_session="fetch")
            await session.execute(query)
            await db.commit_rollback()

    @classmethod
    async def delete(cls, model_id: str):
        async with db as session:
            query = sql_delete(cls.model).where(cls.model.id == model_id)
            await session.execute(query)
            await db.commit_rollback()