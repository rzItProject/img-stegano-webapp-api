
from sqlalchemy.future import select
from app.api.schema.pydantic import UserType
from app.infrastructure.database.model.person import Person
from app.infrastructure.database.model.users import Users
from app.infrastructure.database.repository.user import UsersRepository

from app.infrastructure.database.session import db


class UserService:

    @staticmethod
    async def fetch_user_profile(username:str):
        async with db as session:
            query = select(Users.username, 
                            Users.email, 
                            Person.name, 
                            Person.birth,
                            Person.sex,
                            Person.profile,
                            Person.phone_number).join_from(Users,Person).where(Users.username == username)
            return(await session.execute(query)).mappings().one()
    
    @staticmethod
    async def fetch_all_users() -> list[Users]:
        list_users = await UsersRepository.get_all()
        print(list_users)
        return [UserType(id=user.id, email=user.email, username=user.username) for user in list_users]
    