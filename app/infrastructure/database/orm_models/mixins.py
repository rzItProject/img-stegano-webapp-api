from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from sqlmodel import Field


class TimeMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(
        sa_column=Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)
    )