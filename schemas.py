from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AuthorBaseSchema(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreateSchema(AuthorBaseSchema):
    pass


class AuthorSchema(AuthorBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BookBaseSchema(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: Optional[date] = None
    author_id: int


class BookCreateSchema(BookBaseSchema):
    pass


class BookSchema(BookBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
    