from datetime import datetime

from pydantic import BaseModel


class BookBase(BaseModel):
    title = str
    summary = str
    publication_date = datetime


class BookCreate(BookBase):
    author_id: int


class BookList(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorList(AuthorBase):
    id: int
    books: list[BookList] = []

    class Config:
        orm_mode = True
