from datetime import date

from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int


class BookCreate(BookBase):
    ...


class BookList(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    ...


class AuthorList(AuthorBase):
    id: int
    books: list[BookList]
    model_config = ConfigDict(from_attributes=True)
