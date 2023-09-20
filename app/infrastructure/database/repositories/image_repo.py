from app.infrastructure.database.orm_models.image import Image
from app.infrastructure.database.repositories.base_repo_crud import BaseCrud

class ImageRepository(BaseCrud):
    model = Image
