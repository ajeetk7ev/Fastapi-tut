from datetime import datetime, timezone

from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    content: str = Field(min_length=5, max_length=100)
    author: str = Field(min_length=5, max_length=100)
    date_posted: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )