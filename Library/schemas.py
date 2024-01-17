import datetime

from pydantic import BaseModel

from Library.models import Book


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorRetrieve(AuthorBase):
    id: int
    book: list[Book] = []

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date


class BookCreate(BookBase):
    author_id: int


class BookRetrieve(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True
