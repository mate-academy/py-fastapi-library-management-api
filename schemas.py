from pydantic import BaseModel

from datetime import date


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    publication_date: date
    author: Author
    

    class Config:
        orm_mode = True
