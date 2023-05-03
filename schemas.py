from datetime import date
from typing import Optional, Union

from pydantic import BaseModel, validator
from pydantic.datetime_parse import datetime


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: Optional[Union[date, str]]
    author_id: int

    @validator("publication_date", pre=True)
    def string_to_datetime(cls, v):
        if isinstance(v, str):
            return datetime.fromisoformat(v)
        return v


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True
