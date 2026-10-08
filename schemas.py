import datetime

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author: Author
