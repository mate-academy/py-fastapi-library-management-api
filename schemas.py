import datetime

from pydantic import BaseModel

from models import Book, Author


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorMain(AuthorBase):
    id: int
    books: list[Book] = []

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str = None
    publication_date: datetime.date = datetime.date.today()


class BookCreate(BookBase):
    pass


class BookMain(BookBase):
    id: str
    authors: list[Author]

    class Config:
        orm_mode = True
