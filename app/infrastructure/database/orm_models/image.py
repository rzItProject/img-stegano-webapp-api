from typing import Optional
from sqlalchemy import Column, ForeignKey, String
from sqlmodel import Field, Relationship, SQLModel

from app.infrastructure.database.orm_models.mixins import TimeMixin


class Image(SQLModel, TimeMixin, table=True):
    __tablename__ = "images"
    id: Optional[str] = Field(None, primary_key=True, nullable=False)
    image_link: str
    image_data: str

    user_id: Optional[str] = Field(None,
        sa_column=Column(String, ForeignKey("users.id", ondelete="CASCADE"))
    )

    user: Optional["Users"] = Relationship(back_populates="images")
    signature: Optional["Signature"] = Relationship(back_populates="image")
