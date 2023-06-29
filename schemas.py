from datetime import datetime

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorBaseCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime | None = None


class BookBaseCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True
