from datetime import date

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: str


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class AuthorCreate(AuthorBase):
    pass


class BookCreate(BookBase):
    author_id: int


class BookRead(BookBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class AuthorRead(AuthorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    books: BookRead
