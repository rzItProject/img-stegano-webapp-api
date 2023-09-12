from typing import List
import strawberry

from app.schema.strawberry import (
    UserUpdateInput,
    UserType,
)
from app.service.user import UserService



@strawberry.type
class Query:
    @strawberry.field
    async def get_all(self) -> List[UserType] :
        return await UserService.fetch_all_users()


@strawberry.type
class Mutation:
        
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
