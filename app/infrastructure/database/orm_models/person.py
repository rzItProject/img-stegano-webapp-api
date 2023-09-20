from datetime import date
import string
from typing import Optional
from sqlalchemy import Column, Enum, ForeignKey, String
from sqlmodel import SQLModel, Field, Relationship

from app.infrastructure.database.orm_models.mixins import TimeMixin


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NONBINARY = "NONBINARY"


class Person(SQLModel, TimeMixin, table=True):
    __tablename__ = "person"

    id: Optional[str] = Field(default=None, primary_key=True, nullable=False)
    # first_name: str
    # last_name: str
    name: str
    birthdate: date
    gender: Gender
    profile_picture: Optional[str]

    user_id: Optional[str] = Field(
        None, sa_column=Column(String, ForeignKey("users.id", ondelete="CASCADE"))
    )

    user: Optional["Users"] = Relationship(
        sa_relationship_kwargs={"uselist": False}, back_populates="person"
    )
