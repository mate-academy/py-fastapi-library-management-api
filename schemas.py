from datetime import date

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    bio: str


class Author(AuthorBase):
    id: int
    bio: str
    books: list[Book] = []

    class Config:
        orm_mode = True
