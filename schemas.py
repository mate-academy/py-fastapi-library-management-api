import datetime

from pydantic import BaseModel


class AuthorsBookList(BaseModel):
    id: int
    title: str
    summary: str
    publication_date: datetime.date


class BookAuthorSchema(BaseModel):
    id: int
    name: str


class AuthorRequestSchema(BaseModel):
    name: str
    bio: str


class AuthorResponseSchema(BaseModel):
    id: int
    name: str
    bio: str
    books: list[AuthorsBookList]


class BookRequestSchema(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date
    author_id: int


class BookResponseSchema(BaseModel):
    id: int
    title: str
    summary: str
    publication_date: datetime.date
    author_id: int


class DetailBookResponseSchema(BaseModel):
    id: int
    title: str
    summary: str
    publication_date: datetime.date
    author: BookAuthorSchema
