from datetime import date

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    name: str
    bio: str


class AuthorDelete(BaseModel):
    id: int


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
        orm_mode = True


class BookUpdate(BookBase):
    title: str
    summary: str
    publication_date: date
    author_id: int
