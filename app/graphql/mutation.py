import strawberry

from app.schema.user import UserRegistrationInput, UserUpdateInput, UserType, UserLoginInput, LoginResponse
from app.service.user import UserService

@strawberry.type
class Mutation:
        
    @strawberry.mutation
    async def register_user(self, user_data: UserRegistrationInput) -> UserType:
        try:
            """Registers a new user and returns their details."""
            return await UserService.register_user(user_data)
        except Exception as e:
            raise e
    
    @strawberry.mutation
    async def login_for_access_token(self, user_data: UserLoginInput) -> LoginResponse:
        try:
            """Authenticate a user and return an access token."""
            return await UserService.authenticate_user(user_data.email, user_data.password)
        except Exception as e:
            raise e

    
    @strawberry.mutation
    async def update_user(self, user_id: int, user_data: UserUpdateInput) -> str:
        try:
            """Update a new user and returns their details."""
            return await UserService.update_user(user_id, user_data)
        except Exception as e:
            raise e
        
    @strawberry.mutation
    async def delete_user(self, user_id: int) -> str:
        try:
            """Delete a new user and returns their details."""
            return await UserService.delete_user(user_id)
        except Exception as e:
            raise e

