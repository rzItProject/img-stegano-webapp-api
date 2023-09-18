from typing import List
import strawberry
from app.api.schema.strawberry import ForgotPasswordSchema, ResponseSchemaGql

from app.api.schema.strawberry import (
    UserUpdateInput,
    UserType,
)
from app.service.authentication import AuthService
from app.service.user import UserService



@strawberry.type
class Query:
    @strawberry.field
    async def get_all(self) -> List[UserType] :
        return await UserService.fetch_all_users()


@strawberry.type
class Mutation:

    @strawberry.mutation
    async def forgot_password(request_body: ForgotPasswordSchema)-> ResponseSchemaGql[str]:
        await AuthService.forgot_password_service(request_body)
        return ResponseSchemaGql(detail="Successfully update data!")
