from datetime import datetime

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorList(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime
    author_id: int


class BookCreate(BookBase):
    pass


class BookList(BookBase):
    id: int

    class Config:
        orm_mode = True
