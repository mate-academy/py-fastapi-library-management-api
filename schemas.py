from datetime import date
from typing import Optional, Union

from pydantic import BaseModel, validator
from pydantic.schema import datetime


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorUpdate(BaseModel):
    name: Optional[str]
    bio: Optional[str]


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: Union[date, str]
    author_id: Optional[int]

    @property
    def publication_date_formatted(self) -> str:
        return self.publication_date.strftime("%Y-%m-%d")

    class Config:
        orm_mode = True


class BookUpdate(BaseModel):
    title: Optional[str]
    summary: Optional[str]
    publication_date: Optional[Union[date, str]]
    author_id: Optional[int]


class BookCreate(BaseModel):
    title: str
    summary: str
    publication_date: Union[date, str]
    author_id: int

    @validator("publication_date", pre=True)
    def parse_publication_date(cls, value):
        if isinstance(value, datetime):
            return value.date()
        elif isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d").date()
        else:
            raise ValueError("Invalid publication date format")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Example Book",
                "summary": "This is an example book",
                "publication_date": "2022-05-03",
                "author_id": 1,
            }
        }


class Book(BookBase):
    id: int
    author: Optional[Author]

    class Config:
        orm_mode = True
