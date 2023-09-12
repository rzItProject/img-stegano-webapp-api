from typing import List
from sqlalchemy.future import select

from app.core.db_config import db
from app.model.role import Role
from app.repository.base_repo_crud import BaseCrud


class RoleRepository(BaseCrud):
    model = Role

    @staticmethod
    async def find_by_role_name(role_name:str):
        async with db as session:
            query = select(Role).where(Role.role_name == role_name)
            return (await session.execute(query)).scalar_one_or_none()

    @staticmethod
    async def find_by_list_role_name(role_name:List[str]):
        async with db as session:
            query =  select(Role).where(Role.role_name.in_(role_name))
            return (await session.execute(query)).scalars().all()

    @staticmethod
    async def create_list(role_name: List[Role]):
        async with db as session:
            session.add_all(role_name)
            await db.commit_rollback()
