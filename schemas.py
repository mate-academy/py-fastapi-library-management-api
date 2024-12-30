from datetime import date
from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int


class BookBaseCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorBaseCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list[Book]

    class Config:
        from_attributes = True
