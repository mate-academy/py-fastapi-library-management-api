from datetime import date
from pydantic import BaseModel


class AuthorsBase(BaseModel):
    name: str
    bio: str


class AuthorsCreate(AuthorsBase):
    pass


class AuthorsList(AuthorsBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class BookList(BookBase):
    id: int
    author: AuthorsList

    class Config:
        orm_mode = True
