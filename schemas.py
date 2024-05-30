from typing import List

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: str


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author: AuthorBase

    class Config:
        from_attributes = True


class Author(AuthorBase):
    id: int
    books: List[Book]

    class Config:
        from_attributes = True
