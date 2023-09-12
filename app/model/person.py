

from datetime import date
from typing import Optional
from sqlalchemy import Enum, table
from sqlmodel import SQLModel, Field, Relationship
from app.model.mixins import TimeMixin


class Sex(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NONBINARY = "NONBINARY"


class Person(SQLModel, TimeMixin, table=True):
    __tablename__ = "person"

    id: Optional[str] = Field(default=None, primary_key=True, nullable=False)
    name: str
    birth: date
    sex: Sex
    profile: str

    users: Optional["Users"] = Relationship(
        sa_relationship_kwargs={'uselist': False}, back_populates="person")