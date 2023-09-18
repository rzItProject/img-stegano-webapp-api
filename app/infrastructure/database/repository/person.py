

from app.infrastructure.database.model.person import Person
from app.infrastructure.database.repository.base_repo_crud import BaseCrud


class PersonRepository(BaseCrud):
    model = Person