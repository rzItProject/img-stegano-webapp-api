import strawberry
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from app.core.db_config import db
from app.controller.rest_ctrl.auth_endpoints import router as auth_router
from app.schema.pydantic import CreateUserInput
from app.service.user import UserService
from app.controller.graphql_ctrl.user_resolvers import Mutation, Query
from app.utils.auth_middleware import AuthMiddleware

origins= [
    "http://localhost:3000"
]

PRODUCTION = "True"

def init_app():
    # instance
    app = FastAPI(title="Image Steganographie Web App")
    schema = strawberry.Schema(query=Query, mutation=Mutation)
    graphql_app = GraphQLRouter(schema=schema, graphiql=True)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # Add the authentication middleware
    app.add_middleware(AuthMiddleware)

    app.include_router(auth_router)
    app.include_router(graphql_app, prefix="/graphql")

    @app.on_event("startup")
    async def starup():
        await db.create_all()
        populate_user = [
            {"username": "test1", "email": "test1@email.com", "password": "password1"},
            {"username": "kikou", "email": "kikou@email.com", "password": "kikou"},
        ]

        for user_data in populate_user:
            user = CreateUserInput(**user_data)
            await UserService.register_user(user)

    
    @app.on_event("shutdown")
    async def shutdown():
        await db.drop_all()
        await db.close()

    return app


app = init_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8888, reload=True)
