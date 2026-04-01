from datetime import date

from pydantic import BaseModel, ConfigDict

# Author


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorResponse(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


# Book


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


# Detailed Responses


class AuthorDetailResponse(AuthorResponse):
    books: list[BookResponse] = []
