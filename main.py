import strawberry
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.core.utils.generate_role import generate_role

from app.infrastructure.database.session import db
# from app.api.routes.rest.authentication import router as auth_router
from app.api.routes.rest.login_controller import router as auth_router
from app.api.routes.rest.image_controller import router as image_router
from app.api.routes.graphql.user_resolvers import Mutation, Query
from app.api.dependencies.auth_middleware import AuthMiddleware

origins= [
    "http://localhost:3000",
    "https://localhost:3000",
    "https://192.168.56.1:3000"
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

    # app.include_router(auth_router)
    app.include_router(auth_router)
    app.include_router(image_router)

    app.include_router(graphql_app, prefix="/graphql")

    @app.on_event("startup")
    async def starup():
        await db.create_all()
        await generate_role()
    
    @app.on_event("shutdown")
    async def shutdown():
        await db.drop_all()
        await db.close()
        
    
    return app


app = init_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8888, reload=True)
