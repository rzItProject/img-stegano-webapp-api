from typing import Optional
from sqlalchemy import Column, ForeignKey, String
from sqlmodel import Field, Relationship, SQLModel

from app.infrastructure.database.orm_models.mixins import TimeMixin


class Signature(SQLModel, TimeMixin, table=True):
    __tablename__ = "signatures"
    id: Optional[str] = Field(default=None, primary_key=True, nullable=False)

    image_id: Optional[str] = Field(
        None, sa_column=Column(String, ForeignKey("images.id", ondelete="CASCADE"))
    )

    signature_data: str
    steganography_method: str
    image: Optional["Image"] = Relationship(back_populates="signature")
