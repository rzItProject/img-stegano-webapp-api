from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field

from app.infrastructure.database.model.mixins import TimeMixin
from app.infrastructure.database.model.user_role import UsersRole


class Role(SQLModel,TimeMixin, table=True):
    __tablename__ = "role"

    id: Optional[str] = Field(default=None,primary_key=True, nullable=False)
    role_name: str

    users: List["Users"] = Relationship(back_populates="roles", link_model=UsersRole)