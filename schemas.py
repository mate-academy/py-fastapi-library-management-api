import datetime

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author: AuthorCreate

    class Config:
        from_attributes = True


class Author(AuthorBase):
    id: int
    books: list[BookBase]

    class Config:
        from_attributes = True
