import datetime

from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date | None


class BookCreate(BookBase):
    author_id: int


class BookUpdate(BookBase):
    author_id: int


class Book(BookBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    author: "AuthorName"


class BookName(BaseModel):
    title: str


class BookId(BaseModel):
    id: str


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass


class Author(AuthorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    books: list[BookName]


class AuthorName(BaseModel):
    name: str
