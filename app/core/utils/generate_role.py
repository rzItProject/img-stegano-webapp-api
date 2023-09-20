from uuid import uuid4
from app.infrastructure.database.repositories.role import RoleRepository
from app.infrastructure.database.orm_models.role import Role


async def generate_role():
    _role = await RoleRepository.find_by_list_role_name(["admin", "user"])
    if not _role:
        await RoleRepository.create_list(
            [Role(id=str(uuid4()), role_name="admin"), Role(id=str(uuid4()), role_name="user")])
