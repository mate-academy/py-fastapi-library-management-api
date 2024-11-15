from datetime import date

from pydantic import BaseModel


class AuthorSCHBase(BaseModel):
    name: str
    bio: str


class AuthorSCHCreate(AuthorSCHBase):
    pass


class AuthorSCH(AuthorSCHBase):
    id: int

    class Config:
        orm_mode = True


class BookSCHBase(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int


class BookSCHCreate(BookSCHBase):
    pass


class BookSCH(BookSCHBase):
    id: int
    author: AuthorSCH

    class Config:
        orm_mode = True
