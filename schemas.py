import datetime

from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    summary: str | None = None
    publication_date: datetime.date

class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    publication_date: datetime.date
    author_id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list[Book]

    model_config = ConfigDict(from_attributes=True)



