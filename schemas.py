import datetime

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorMain(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date = None


class BookCreate(BookBase):
    pass


class BookMain(BookBase):
    id: int
    authors: list[AuthorMain] = []

    class Config:
        orm_mode = True
