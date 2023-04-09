import datetime

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date


class BookCreate(BookBase):
    pass


class BookList(BookBase):
    id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorList(AuthorBase):
    id: int
    books: list[BookList] = []

    class Config:
        orm_mode = True
