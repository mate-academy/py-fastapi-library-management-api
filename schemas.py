from pydantic import BaseModel, ConfigDict
from datetime import date


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorResponse(AuthorBase):
    id: int
    books: list[BookResponse] = []

    model_config = ConfigDict(from_attributes=True)
