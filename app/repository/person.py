from app.model.person import Person
from app.repository.base_repo_crud import BaseCrud

class PersonRepository(BaseCrud):
    model = Person