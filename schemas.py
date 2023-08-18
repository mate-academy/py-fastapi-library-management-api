import datetime

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreateUpdate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date


class BookCreateUpdate(BookBase):
    author_id: int | None = None


class Book(BookBase):
    id: int
    author: AuthorBase

    class Config:
        from_attributes = True
