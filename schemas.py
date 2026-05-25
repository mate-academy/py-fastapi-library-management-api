from datetime import date

from pydantic import BaseModel


# Author
class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorResponse(AuthorBase):
    id: int

    class Config:
        orm_mode = True


# Book
class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class BookResponse(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True
