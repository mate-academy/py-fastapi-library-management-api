from pydantic import BaseModel

import models


class AuthorBase(BaseModel):
    name: str
    biography: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list[models.Book] = []

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: str


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True
