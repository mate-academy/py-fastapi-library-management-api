from datetime import date

from pydantic import BaseModel

from models import DBBook


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list[DBBook] = []

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str | None = None
    publication_date: date
    author_id: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author: Author

    class Config:
        orm_mode = True
