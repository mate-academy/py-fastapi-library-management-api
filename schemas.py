from datetime import date
from typing import List, Optional
from pydantic import BaseModel, field_validator


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    bio: Optional[str] = None
    books: List[int] = []

class AuthorListItem(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class AuthorList(BaseModel):
    authors: List[AuthorListItem]


class AuthorRetrieve(AuthorBase):
    id: int
    bio: Optional[str] = None

    class Config:
        from_attributes = True


class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None


class BookBase(BaseModel):
    title: str


class BookCreate(BookBase):
    summary: Optional[str] = None
    publication_date: date
    author_id: int

    @field_validator("publication_date", mode="before")
    @classmethod
    def publication_date_validation(cls, value: date) -> date:
        if value < date.today():
            raise ValueError("The publication date cannot be earlier than today")
        return value


class BookListItem(BookBase):
    id: int

    class Config:
        from_attributes = True


class BookList(BaseModel):
    books: List[BookListItem]


class BookRetrieve(BookBase):
    id: int
    summary: Optional[str] = None
    publication_date: date
    author_id: int

    class Config:
        from_attributes = True


class BookUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    publication_date: Optional[date] = None
    author_id: Optional[int] = None
