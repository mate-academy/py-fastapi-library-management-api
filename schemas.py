from datetime import date

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorList(AuthorBase):
    id: int

    class Config:
        orm_model = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class BookList(BookBase):
    id: int
    author: AuthorList

    class Config:
        orm_mode = True
