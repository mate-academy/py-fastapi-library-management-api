import datetime

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    bio: str | None = None
    publication_date: datetime.date | None = None

    class Config:
        from_attributes = True


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author: Author
