from fastapi import Depends
from app.core.use_cases.auth.login_uc import LoginUseCase
from app.core.use_cases.auth.register_uc import RegisterUseCase
from app.api.auth_repo import JWTRepo

from app.infrastructure.database.repositories.person import PersonRepository
from app.infrastructure.database.repositories.role import RoleRepository
from app.infrastructure.database.repositories.user import UsersRepository
from app.infrastructure.database.repositories.user_role import UsersRoleRepository


def get_person_repository():
    return PersonRepository()


def get_user_repository():
    return UsersRepository()


def get_role_repository():
    return RoleRepository()


def get_user_role_repository():
    return UsersRoleRepository()


def get_token_repository():
    return JWTRepo()


def get_login_uc(
    user_repo: UsersRepository = Depends(get_user_repository),
    token_service: JWTRepo = Depends(get_token_repository),
) -> LoginUseCase:
    return LoginUseCase(user_repo, token_service)


def get_register_uc(
    person_repo: PersonRepository = Depends(get_person_repository),
    user_repo: UsersRepository = Depends(get_user_repository),
    role_repo: RoleRepository = Depends(get_role_repository),
    user_role_repo: UsersRoleRepository = Depends(get_user_role_repository),
) -> RegisterUseCase:
    return RegisterUseCase(person_repo, user_repo, role_repo, user_role_repo)
