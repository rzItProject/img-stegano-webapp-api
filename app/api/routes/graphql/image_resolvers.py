from fastapi import UploadFile
import strawberry

@strawberry.input
class ImageUploadInput:
    file: UploadFile

@strawberry.type
class ImageUploadResponse:
    filename: str
    url: str  # URL de l'image sur S3 ou autre message de réussite/erreur
    status: str

@strawberry.type
class Mutation:
    @strawberry.mutation
    def upload_image(self, input: ImageUploadInput) -> ImageUploadResponse:
        #success = save_to_s3(input.file, "your-bucket-name", input.file.filename)
        success = "your-bucket-name"
        if success:
            url = f"https://your-bucket-name.s3.amazonaws.com/{input.file.filename}"  # Modifiez l'URL selon votre configuration S3
            return ImageUploadResponse(filename=input.file.filename, url=url, status="success")
        else:
            return ImageUploadResponse(filename=input.file.filename, url="", status="failed")

