from datetime import datetime, date

from pydantic import BaseModel
from pydantic.v1 import validator


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BaseModel):
    title: str
    publication_date: date | int
    author_id: int
    summary: str

    @validator("publication_date", pre=True)
    def parse_publication_date(cls, value):
        if isinstance(value, int):
            return datetime.utcfromtimestamp(value / 1000).date()
        return value


class Book(BookBase):
    id: int
    author: Author

    class Config:
        from_attributes = True
