from typing import List
from uuid import uuid4
from fastapi import HTTPException, UploadFile
from psycopg2 import DatabaseError
from app.api.schema.pydantic import ImageResponseModel
from app.infrastructure.database.orm_models.image import Image
from app.infrastructure.database.repositories.image import ImageRepository
from app.infrastructure.storage.s3_repository import S3Repository

BUCKET_NAME = "stegano"


class S3UseCase:
    def __init__(self, s3_repository: S3Repository, image_repository: ImageRepository):
        self.s3_repository = s3_repository
        self.image_repository = image_repository

    async def execute_get_user_image_by_id(self, image_id: str):
        image = await self.image_repository.get_image_by_id(image_id)
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        url = self.execute_generate_url(BUCKET_NAME, image.image_data)
        return ImageResponseModel(
            id=image.id, image_data=image.image_data, image_link=url
        )

    async def execute_get_all_images(self):
        try:
            images = await self.image_repository.get_all()
            if not images:
                raise HTTPException(
                    status_code=404, detail="No images found in the database."
                )
            images_url: List[ImageResponseModel] = []
            for image in images:
                url = self.execute_generate_url(BUCKET_NAME, image.image_data)
                images_url.append(
                    {"id": image.id, "image_link": url, "image_data": image.image_data}
                )
            return images_url
        except DatabaseError as e:
            # Vous pouvez logger l'erreur `e` ici si nécessaire
            raise HTTPException("Error accessing the database.")

    async def execute_get_user_images(self, user_id: str):
        images = await self.image_repository.get_images_by_user_id(user_id)
        if not images:
            raise HTTPException(
                status_code=404, detail="No images found in the database."
            )
        images_url: List[ImageResponseModel] = []
        for image in images:
            url = self.execute_generate_url(BUCKET_NAME, image.image_data)
            images_url.append(
                {"id": image.id, "image_link": url, "image_data": image.image_data}
            )
        return images_url

    async def execute_upload(self, user_id: str, file):
        # Upload to S3
        self.s3_repository.upload_file(BUCKET_NAME, file.file, file.filename)

        _image_id = str(uuid4())
        # Save to DB
        _image = Image(
            id=_image_id,
            image_link=f"https://s3.tebi.io/{BUCKET_NAME}/{file.filename}",
            image_data=file.filename,
            user_id=user_id,
        )

        # Vérifier si le nom de l'image existe déjà
        existing_image = await self.image_repository.find_by_image_name(
            _image.image_data
        )
        if existing_image:
            raise HTTPException(status_code=400, detail="Image name already exists!")

        await self.image_repository.create(**_image.dict())

    def execute_list_buckets(self):
        return self.s3_repository.list_buckets()

    def execute_download(self, bucket_name: str, key: str, output_path: str):
        self.s3_repository.download_file(bucket_name, key, output_path)

    def execute_generate_url(self, bucket_name: str, object_name: str):
        return self.s3_repository.generate_presigned_url(bucket_name, object_name)
