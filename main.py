import strawberry
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import userRoute
from app.database.config import db
from app.graphql.query import Query
from strawberry.fastapi import GraphQLRouter

def init_app():
    # instance
    apps = FastAPI()

    # config static and templates
    templates = Jinja2Templates(directory="app/templates")
    apps.mount("/app/static", StaticFiles(directory="app/static"), name="static")

    @apps.on_event("startup")
    async def startup():
        await db.create_all()

    @apps.on_event("shutdown")
    async def shutdown():
        await db.drop_all() 

    # add graphql endpoint
    schema = strawberry.Schema(query=Query)
    graphql_app = GraphQLRouter(schema)
    
    apps.include_router(graphql_app, prefix="/graphql")
    apps.include_router(userRoute.userRouter)

    return apps


app = init_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8888, reload=True)
