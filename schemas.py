from datetime import date

from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class AuthorBase(BaseModel):
    name: Annotated[str, Field(max_length=100)]
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: Annotated[str, Field(max_length=255)]
    summary: Annotated[str, Field(max_length=511)]
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class BookRead(BookBase):
    id: int
    author: AuthorRead
    model_config = ConfigDict(from_attributes=True)
