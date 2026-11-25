from pydantic import BaseModel, ConfigDict
from datetime import date, datetime

class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int
    books: list[BookBase]

    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class BookRead(BookBase):
    id: int
    author: AuthorRead

    model_config = ConfigDict(from_attributes=True)
