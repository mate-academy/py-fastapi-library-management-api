from datetime import date

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str = None
    publication_date: date = None
    author_id: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author: Author

    class Config:
        orm_mode = True
