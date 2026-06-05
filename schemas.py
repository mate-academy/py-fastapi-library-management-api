from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime


class BookCreate(BookBase):
    author_id: int | None = None


class BookCreateInAuthor(BookBase):
    pass


class Book(BookBase):
    model_config = ConfigDict(from_attributes=True)
    author_id: int | None = None
    id: int


class BookUpdate(BookBase):
    author_id: int | None = None


class BookPartialUpdate(BaseModel):
    title: str | None = None
    summary: str | None = None
    publication_date: datetime | None = None
    author_id: int | None = None


class BookReference(BaseModel):
    id: int


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    books: list[BookCreateInAuthor] | None = None


class Author(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    books: list[Book]


class AuthorUpdate(AuthorCreate):
    books: list[BookReference] | None = None


class AuthorPartialUpdate(BaseModel):
    name: str | None = None
    bio: str | None = None
    books: list[BookReference] = None
