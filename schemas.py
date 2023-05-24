from datetime import datetime

from pydantic import BaseModel

from db.models import Book


class AuthorBase(BaseModel):
    name: str
    bio: str
    book: list[Book] = []

    class Config:
        arbitrary_types_allowed = True


class CreateAuthor(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class UpdateAuthor(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime
    author_id: int


class CreateBook(BookBase):
    id: int

    class Config:
        orm_mode = True


class UpdateBook(BookBase):
    id: int

    class Config:
        orm_mode = True
