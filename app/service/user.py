from app.repository.user import UserRepository
from app.schema.strawberry import UserUpdateInput
from app.schema.pydantic import CreateUserInput, LoginUserInput, UserType
from app.model.user import User
from app.utils.security import hash_password, verify_password

# Custom Exception Classes
class AuthenticationError(Exception):
    pass

class UserAlreadyExistsError(Exception):
    pass

class UserNotFoundError(Exception):
    pass


class UserService:

    @staticmethod
    async def register_user(user_data: CreateUserInput) -> UserType:
        # Check if a user with the given email already exists.
        existing_user = await UserRepository.get_user_by_email(user_data.email)
        if existing_user:
            raise UserAlreadyExistsError("A user with this email already exists.")
        new_user = User()
        new_user.username = user_data.username
        new_user.email = user_data.email
        new_user.hashed_password = hash_password(user_data.password)
        #new_user = User(username=user_data.username, email=user_data.email, hashed_password=hash_password(user_data.password))

        # Save the user to the database.
        await UserRepository.create_user(new_user)

        return UserType(id=new_user.id, email=new_user.email, username=new_user.username)
    
    @staticmethod
    async def authenticate_user(user_data: LoginUserInput) -> User:
        user = await UserRepository.get_user_by_username(user_data.username)
        if not user:
            # raise StrawberryGraphQLError(message="Could not validate user.")
            return False
        
        if not verify_password(user_data.password, user.hashed_password):
            # raise AuthenticationError("Invalid email or password.")
            return False
        
        return user
        #access_token = create_access_token(data={"sub": user.id, "username": user.username}, expires_delta=timedelta(minutes=10))
        # return LoginResponse(access_token=access_token, message="Login Succesfull")
        #return {"user": user, "access_token": access_token}
    
    @staticmethod
    async def fetch_all_users() -> list[User]:
        list_users = await UserRepository.get_all_users()
        return [UserType(id=user.id, email=user.email, username=user.username) for user in list_users]
    
    @staticmethod
    async def fetch_user_by_id(user_id: int) -> User:
        user = await UserRepository.get_user_by_id(user_id)
        return UserType(id=user.id, email=user.email, username=user.username)
    
    @staticmethod
    async def fetch_user_by_email(email: str) -> User:
        user = await UserRepository.get_user_by_email(email)
        return UserType(id=user.id, email=user.email, username=user.username)
    
    @staticmethod
    async def fetch_user_by_username(username: str) -> User:
        return await UserRepository.get_user_by_username(username)
        # return UserLoginInput(username=user.username, password=user.hashed_password)

    @staticmethod
    async def update_user(user_id: int, user_data: UserUpdateInput) -> str:
        user = await UserRepository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"UPDATE USER> User with ID {user_id} not found.")
        
        if user_data.username:
            user.username = user_data.username
        if user_data.email:
            user.email = user_data.email
        if user_data.password:
            user.email = hash_password(user_data.email)

        # Save the changes (assuming you have a method for this in UserRepository)
        await UserRepository.update_user(user_id, user)
        return f'Successfully updated data by id {user_id}'
    
    @staticmethod
    async def delete_user(user_id: int) -> str:
        user = await UserRepository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"DELETE USER> User with ID {user_id} not found.")
        await UserRepository.delete_user(user_id)
        return f'Successfully deleted data by id {user_id}'