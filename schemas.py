from datetime import date

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date

    class Config:
        orm_mode = True


class BookCreate(BookBase):
    author_id: int


class BookUpdate(BookBase):
    pass


class Book(BookBase):
    id: int


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None

    class Config:
        orm_mode = True


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list[Book] = []
