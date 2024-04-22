from datetime import date
from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class Author(AuthorBase):
    id: int
    books: list[BookBase]

    class Config:
        from_attributes = True


class Book(BookBase):
    id: int
    author: Author

    class Config:
        from_attributes = True
