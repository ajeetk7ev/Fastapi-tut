
from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class PostBase(BaseModel):
    author: str = Field(..., min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)


class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    author: str | None = Field(default=None, min_length=1, max_length=100)
    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = Field(default=None, min_length=1)

    model_config = ConfigDict(extra="forbid")
    
class PostResponse(PostBase):
    id: int
    date_posted: date

    model_config = ConfigDict(from_attributes=True)
