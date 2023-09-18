from typing import Optional
from sqlalchemy import Column, ForeignKey, String
from sqlmodel import Field, SQLModel

from app.infrastructure.database.model.mixins import TimeMixin


class UsersRole(SQLModel,TimeMixin, table=True):
    __tablename__ = "user_role"
    users_id: Optional[str] = Field(
        default=None,
        sa_column=Column(
            String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
        ),
    )

    role_id: Optional[str] = Field(
        default=None,
        sa_column=Column(
            String, ForeignKey("role.id", ondelete="CASCADE"), primary_key=True
        ),
    )
