from app.infrastructure.database.orm_models.image import Image
from app.infrastructure.database.repositories.base_repo_crud import BaseCrud
from app.infrastructure.database.session import db
from sqlalchemy.future import select


class ImageRepository(BaseCrud):
    model = Image

    @staticmethod
    async def find_by_image_name(image_name: str):
        async with db as session:
            query = select(Image).where(Image.image_data == image_name)
            return (await session.execute(query)).scalar_one_or_none()

    @staticmethod
    async def get_image_by_id(image_id: str):
        async with db as session:
            query = select(Image).where(Image.id == image_id)
            return (await session.execute(query)).scalar_one_or_none()

    @staticmethod
    async def get_images_by_user_id(user_id: str):
        async with db as session:
            query = select(Image).where(Image.user_id == user_id)
            return (await session.execute(query)).scalars().all()
