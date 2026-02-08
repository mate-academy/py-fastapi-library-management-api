import datetime

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):

    title: str
    summary: str
    publication_date: datetime.date


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: int
    model_config = ConfigDict(from_attributes=True)


class AuthorWithBooks(Author):
    books: list[Book] = []
