from typing import List, Optional
from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field, Relationship

from app.infrastructure.database.orm_models.mixins import TimeMixin
from app.infrastructure.database.orm_models.user_role import UsersRole


class Users(SQLModel, TimeMixin, table=True):
    __tablename__ = "users"

    id: Optional[str] = Field(None, primary_key=True, nullable=False)
    username: str = Field(sa_column=Column("username", String, unique=True))
    email: str = Field(sa_column=Column("email", String, unique=True))
    password: str

    person: Optional["Person"] = Relationship(back_populates="user")
    images: List["Image"] = Relationship(back_populates="user")
    roles: List["Role"] = Relationship(back_populates="users", link_model=UsersRole)
