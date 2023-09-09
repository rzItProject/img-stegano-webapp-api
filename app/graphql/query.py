from typing import List
import strawberry
from app.service.user import UserService
from app.schema.user import UserType

@strawberry.type
class Query:

    @strawberry.field
    def hello(self) -> str:
        return "Hello World !"

    @strawberry.field
    async def get_all(self) -> List[UserType] :
        return await UserService.fetch_all_users()
    
    """ @strawberry.field
    async def get_user_by_id(self, id: int) -> UserType:
        return await UserService.get_user_by_id(id) """
