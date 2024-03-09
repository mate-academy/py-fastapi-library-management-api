from datetime import date

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class AuthorCreate(AuthorBase):
    pass


class Book(BookBase):
    id: int
    author: AuthorBase

    class Config:
        orm_mode = True


class BookCreate(BookBase):
    author_id: int


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True
