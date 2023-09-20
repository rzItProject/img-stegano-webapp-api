from typing import List
from sqlalchemy.future import select
from app.infrastructure.database.orm_models.role import Role
from app.infrastructure.database.repositories.base_repo_crud import BaseCrud

from app.infrastructure.database.session import db



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
