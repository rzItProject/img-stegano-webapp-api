from uuid import uuid4
from fastapi import HTTPException, UploadFile
from app.infrastructure.database.orm_models.image import Image
from app.infrastructure.database.repositories.image import ImageRepository
from app.infrastructure.storage.s3_repository import S3Repository


class S3UseCase:
    def __init__(self, s3_repository: S3Repository, image_repository: ImageRepository):
        self.s3_repository = s3_repository
        self.image_repository = image_repository
    
    async def get_single_image(self, image_id: str):
        image = await self.image_repository.get_image_by_id(image_id)
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        return image
    
    async def execute_get_user_images(self, user_id: str):
        return await self.image_repository.get_images_by_user_id(user_id)

    async def execute_upload(self, user_id: str, file):
        # Upload to S3
        self.s3_repository.upload_file("stegano", file.file, file.filename)

        _image_id = str(uuid4())
        # Save to DB
        _image = Image(
            id=_image_id,
            image_link=f"https://s3.tebi.io/stegano/{file.filename}",
            image_data=file.filename,
            user_id=user_id,
        )

        # Vérifier si le nom de l'image existe déjà
        existing_image = await self.image_repository.find_by_image_name(_image.image_data)
        if existing_image:
            raise HTTPException(status_code=400, detail="Image name already exists!")

        await self.image_repository.create(**_image.dict())

    def execute_list_buckets(self):
        return self.s3_repository.list_buckets()

    def execute_download(self, bucket_name: str, key: str, output_path: str):
        self.s3_repository.download_file(bucket_name, key, output_path)
