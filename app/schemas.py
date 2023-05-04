from pydantic import BaseModel
from datetime import date


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookPartialUpdate(BaseModel):
    title: str | None
    summary: str | None
    publication_date: date | None


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass


class AuthorPartialUpdate(BaseModel):
    name: str | None
    bio: str | None


class Author(AuthorBase):
    id: int
    books: list[Book] = []

    class Config:
        orm_mode = True
