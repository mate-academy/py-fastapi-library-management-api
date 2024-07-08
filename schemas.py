from datetime import date

from pydantic import BaseModel, Field


class AuthorBase(BaseModel):
    name: str
    bio: str


class Author(AuthorBase):
    id: int
    books: list["Book"]

    class Config:
        orm_mode = True


class AuthorCreate(AuthorBase):
    pass


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class BookCreate(BookBase):
    pass
