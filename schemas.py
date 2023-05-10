import datetime

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str

    class Config:
        orm_mode = True


class Author(AuthorBase):
    id: int


class AuthorCreate(AuthorBase):
    pass


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date
    author_id: int

    class Config:
        orm_mode = True


class Book(BookBase):
    id: int


class BookCreate(BookBase):
    pass
