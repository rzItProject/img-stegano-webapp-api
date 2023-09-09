from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import uvicorn

from app.routes import userRoute


def init_app():
    # instance
    apps = FastAPI()

    # config static and templates
    templates = Jinja2Templates(directory="app/templates")
    apps.mount("/app/static", StaticFiles(directory="app/static"), name="static")

    apps.include_router(userRoute.userRouter)

    return apps


app = init_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8888, reload=True)
