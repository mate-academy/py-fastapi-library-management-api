from datetime import date

from pydantic import BaseModel


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
    published_date: date


class BookCreate(BookBase):
    author_id: int


class BookCreateForAuthor(BookBase):
    pass


class Book(BookBase):
    id: int
    author: Author

    class Config:
        orm_mode = True
