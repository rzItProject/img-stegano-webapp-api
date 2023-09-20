from fastapi import APIRouter, Depends, File, UploadFile
from app.api.dependencies.token import get_token_from_cookie
from app.api.dependencies.user import get_current_user
from app.infrastructure.database.orm_models.users import Users
from app.infrastructure.database.repositories.image_repo import ImageRepository
from app.infrastructure.storage.s3_repository import S3Repository
from app.core.use_cases.s3_usecase import S3UseCase
import boto3

s3_repository = S3Repository('zYHXMlSzpZDrNrc8', 'ft7TvAGY6aTCOo49M0hS7pJEig8rumbiMNeSiyZy', 'https://s3.tebi.io')
image_repository = ImageRepository()
s3_use_case = S3UseCase(s3_repository, image_repository)

router = APIRouter(tags=["Upload"])

@router.post("/upload/")
async def upload_image_route(file: UploadFile = File(...), user: Users = Depends(get_current_user)):
    await s3_use_case.execute_upload(user.id, file)
    return {"message": "Upload successful", "filename": file.filename, "user_id": user.id}
