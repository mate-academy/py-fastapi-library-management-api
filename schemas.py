from pydantic import BaseModel
from pydantic.types import date


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorRead(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class AuthorCreate(AuthorBase):
    pass


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    pass


class BookList(BookBase):
    id: int
    author: AuthorRead

    class Config:
        orm_mode = True
