from datetime import date
from pydantic import BaseModel


class AuthorName(BaseModel):
    id: int
    name: str


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author: AuthorName

    class Config:
        from_attributes = True


class BookTitle(BaseModel):
    id: int
    title: str


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list[BookTitle] = []

    class Config:
        from_attributes = True
