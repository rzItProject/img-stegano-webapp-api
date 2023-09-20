from fastapi import UploadFile
from app.infrastructure.database.repositories.image_repo import ImageRepository
from app.infrastructure.storage.s3_repository import S3Repository


class S3UseCase:
    def __init__(self, s3_repository: S3Repository, image_repository: ImageRepository):
        self.s3_repository = s3_repository
        self.image_repository = image_repository

    async def execute_upload(self, user_id: str, file):
        # Upload to S3
        self.s3_repository.upload_file('stegano', file.file, file.filename)

        # Save to DB
        image_data = {
            "image_link": f"https://s3.tebi.io/stegano/{file.filename}",
            "image_data": "some_data_here", 
            "user_id": user_id
        }
        #await self.image_repository.save_image_details(image_data)

    def execute_list_buckets(self):
        return self.s3_repository.list_buckets()

    def execute_download(self, bucket_name: str, key: str, output_path: str):
        self.s3_repository.download_file(bucket_name, key, output_path)
