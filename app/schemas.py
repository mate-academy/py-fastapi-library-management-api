from pydantic import BaseModel
from datetime import date


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
    author_id: int


class AuthorBase(BaseModel):
    name: str
    bio: str


class Author(AuthorBase):
    id: int
    books: list[Book] = []

    class Config:
        orm_mode = True


class AuthorCreate(AuthorBase):
    pass
