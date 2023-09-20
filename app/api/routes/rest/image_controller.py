from fastapi import APIRouter, File, UploadFile
from app.infrastructure.database.repositories.image_repo import ImageRepository
from app.infrastructure.storage.s3_repository import S3Repository
from app.core.use_cases.s3_usecase import S3UseCase
import boto3

s3_repository = S3Repository('zYHXMlSzpZDrNrc8', 'ft7TvAGY6aTCOo49M0hS7pJEig8rumbiMNeSiyZy', 'https://s3.tebi.io')
image_repository = ImageRepository()
s3_use_case = S3UseCase(s3_repository, image_repository)

router = APIRouter(tags=["Upload"])

s3 = boto3.client(
    service_name='s3',
    aws_access_key_id='zYHXMlSzpZDrNrc8',
    aws_secret_access_key='ft7TvAGY6aTCOo49M0hS7pJEig8rumbiMNeSiyZy',
    endpoint_url='https://s3.tebi.io'
)

@router.post("/upload/")
def upload_image_route(file: UploadFile = File(...)):
    s3.upload_fileobj(file.file, "stegano", file.filename)
    return {"filename": file.filename}
    #s3_use_case.execute_upload('stegano', file.file, file.filename)
    #return {"message": "Upload successful"}
