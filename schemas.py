from datetime import date

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    name: str | None = None
    bio: str | None = None


class Author(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class BookUpdate(BookBase):
    title: str | None = None
    summary: str | None = None
    publication_date: date | None = None
    author_id: int | None = None


class Book(BookBase):
    id: int
    author: Author

    class Config:
        from_attributes = True
