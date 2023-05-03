from datetime import date

from pydantic import BaseModel


class AuthorNoId(BaseModel):
    name: str
    bio: str

    class Config:
        orm_mode = True


class AuthorWithId(AuthorNoId):
    id: int


class Book(BaseModel):
    title: str
    summary: str
    publication_date: date

    class Config:
        orm_mode = True


class BookNoId(Book):
    author_id: int


class BookWithId(Book):
    id: int
    author: AuthorWithId
