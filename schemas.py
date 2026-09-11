from datetime import date

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorList(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int


class BookCreate(BookBase):
    pass


class BookList(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author: AuthorList
