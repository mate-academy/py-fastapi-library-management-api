from pydantic import BaseModel

from models import DBBook, DBAuthor


class AuthorBase(BaseModel):
    name: str
    bio: str
    books: list[DBBook]


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: str


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author = DBAuthor

    class Config:
        orm_mode = True
