from datetime import date

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    model_config = {"from_attributes": True}


class AuthorUpdate(BaseModel):
    name: str | None = None
    bio: str | None = None

    model_config = {"from_attributes": True, }


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int


class BookUpdate(BaseModel):
    title: str | None = None
    summary: str | None = None
    publication_date: date | None = None
    author_id: int | None = None
