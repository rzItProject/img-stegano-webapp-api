

from app.infrastructure.database.model.user_role import UsersRole
from app.infrastructure.database.repository.base_repo_crud import BaseCrud


class UsersRoleRepository(BaseCrud):
    model = UsersRole