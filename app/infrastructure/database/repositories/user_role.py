

from app.infrastructure.database.orm_models.user_role import UsersRole
from app.infrastructure.database.repositories.base_repo_crud import BaseCrud


class UsersRoleRepository(BaseCrud):
    model = UsersRole