from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuthorShort(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime
    author_id: int


class Book(BookBase):
    id: int
    author: AuthorShort

    model_config = ConfigDict(from_attributes=True)


class BookCreate(BookBase):
    pass


class AuthorBase(BaseModel):
    name: str
    bio: str


class Author(AuthorBase):
    id: int
    books: list[Book]

    model_config = ConfigDict(from_attributes=True)


class AuthorCreate(AuthorBase):
    pass
