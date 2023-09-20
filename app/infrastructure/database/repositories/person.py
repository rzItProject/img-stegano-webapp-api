from app.infrastructure.database.orm_models.person import Person
from app.infrastructure.database.repositories.base_repo_crud import BaseCrud


class PersonRepository(BaseCrud):
    model = Person