from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    pass


class BookOut(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorOut(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class AuthorOutWithBooks(AuthorOut):
    books: list[BookOut] = Field(default_factory=list)
