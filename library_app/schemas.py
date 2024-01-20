from datetime import date

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorRetrieve(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int


class BookCreate(BookBase):
    author_id: int


class BookRetrieve(BookBase):
    id: int
    author: AuthorRetrieve

    class Config:
        from_attributes = True
