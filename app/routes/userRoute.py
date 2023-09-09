from fastapi import APIRouter

# instance
userRouter=APIRouter()

@userRouter.get("/")
async def root():
    return {"message": "Hello World"}