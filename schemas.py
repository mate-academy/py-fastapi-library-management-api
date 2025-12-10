from pydantic import BaseModel, ConfigDict
import datetime


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    books: list["Book"] = []





class BookBase(BaseModel):
    title: str
    summary: str | None = None
    publication_date: datetime.date | None = None


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    model_config = ConfigDict(from_attributes=True)

    author: Author



