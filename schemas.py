import datetime

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date
    author_id: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        from_attributes = True
