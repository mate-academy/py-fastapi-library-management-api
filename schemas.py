from datetime import date

from pydantic import BaseModel
from typing_extensions import List


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date

    class Config:
        from_attributes = True


class BookCreate(BookBase):
    author_id: int


class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True


class BookListResponse(BaseModel):
    books: List[BookResponse]

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    id: int
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorResponse(AuthorBase):
    id: int
    books: List[BookResponse] = []

    class Config:
        from_attributes = True
