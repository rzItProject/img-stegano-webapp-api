import base64
from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException
from passlib.context import CryptContext

from app.api.schema.pydantic import RegisterSchema

from app.infrastructure.database.orm_models.person import Person
from app.infrastructure.database.orm_models.user_role import UsersRole
from app.infrastructure.database.orm_models.users import Users
from app.infrastructure.database.repositories.person import PersonRepository
from app.infrastructure.database.repositories.role import RoleRepository
from app.infrastructure.database.repositories.user import UsersRepository
from app.infrastructure.database.repositories.user_role import UsersRoleRepository

# Encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegisterUseCase:
    def __init__(self, person_repository: PersonRepository, user_repository: UsersRepository, role_repository: RoleRepository, user_role_repository: UsersRoleRepository):
        self.person_repository = person_repository
        self.user_repository = user_repository
        self.role_repository = role_repository
        self.user_role_repository = user_role_repository
    
    async def register(self, register: RegisterSchema):
        # Create uuid
        _person_id = str(uuid4())
        _users_id = str(uuid4())

        # convert birth date type from frontend str to date
        birth_date = datetime.strptime(register.birthdate, "%d-%m-%Y")

        # open image profile default to bas64 string
        """ with open("./img/profile.png", "rb") as f:
            image_str = base64.b64encode(f.read())
        image_str = "data:image/png;base64," + image_str.decode("utf-8") 
        image_str = "data:image/png;base64," """

        # mapping request data to class entity table
        _person = Person(
            id=_person_id,
            name=register.name,
            birthdate=birth_date,
            gender=register.gender,
            profile_picture="image_str",
            user_id=_users_id
        )

        _users = Users(
            id=_users_id,
            username=register.username,
            email=register.email,
            password=pwd_context.hash(register.password),
        )

        # Everyone who registers through our registration page makes the default as a user
        _role = await self.role_repository.find_by_role_name("user")
        _users_role = UsersRole(users_id=_users_id, role_id=_role.id)

        # Cheking the same username
        _username = await self.user_repository.find_by_username(register.username)
        if _username:
            raise HTTPException(status_code=400, detail="Username already exists!")

        # Cheking the same email
        _email = await self.user_repository.find_by_email(register.email)
        if _email:
            raise HTTPException(status_code=400, detail="Email already exists!")
        
        #  insert to tables
        await self.user_repository.create(**_users.dict())
        await self.person_repository.create(**_person.dict())
        await self.user_role_repository.create(**_users_role.dict())

        return _users

