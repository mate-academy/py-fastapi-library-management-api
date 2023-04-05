import datetime

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date

    class Config:
        orm_mode = True


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author_id: int


class AuthorBase(BaseModel):
    name: str
    bio: str

    class Config:
        orm_mode = True


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list[Book] = []
