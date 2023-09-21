import subprocess
from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile
from app.api.dependencies.token import get_token_from_cookie
from app.api.dependencies.user import get_current_user
from app.api.schema.pydantic import ImageResponseModel, ImageUrlResponseModel
from app.infrastructure.database.orm_models.users import Users
from app.infrastructure.database.repositories.image import ImageRepository
from app.infrastructure.storage.s3_repository import S3Repository
from app.core.use_cases.s3_usecase import S3UseCase

s3_repository = S3Repository('zYHXMlSzpZDrNrc8', 'ft7TvAGY6aTCOo49M0hS7pJEig8rumbiMNeSiyZy', 'https://s3.tebi.io')
image_repository = ImageRepository()
s3_use_case = S3UseCase(s3_repository, image_repository)

router = APIRouter(tags=["Upload and Get"])

def run_script():
    subprocess.run(["python", "app/core/utils/signature.py"])

@router.post("/upload/")
async def upload_image(background_tasks: BackgroundTasks, file: UploadFile = File(...), user: Users = Depends(get_current_user)):
    await s3_use_case.execute_upload(user.id, file)
    #background_tasks.add_task(run_script)
    #return {"message": "Script will be executed in the background!"}
    return {"message": "Upload successful", "filename": file.filename, "user_id": user.id}

@router.get("/images/all", response_model=List[ImageResponseModel])
async def get_all_images(current_user: Users = Depends(get_current_user)):
    images = await s3_use_case.execute_get_all_images()
    return images

@router.get("/images", response_model=List[ImageResponseModel])
async def get_all_user_images(current_user: Users = Depends(get_current_user)):
    images = await s3_use_case.execute_get_user_images(current_user.id)
    return images

@router.get("/images/{image_id}", response_model=ImageResponseModel)
async def get_single_user_image(image_id: str):
    image = await s3_use_case.execute_get_user_image_by_id(image_id)
    return image



