from datetime import date
from typing import Optional

from pydantic import BaseModel


class AuthorCreateSchema(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorResponseSchema(BaseModel):
    id: int
    name: str
    bio: Optional[str] = None

    class Config:
        from_attributes = True


class AuthorDetailSchema(BaseModel):
    id: int
    name: str
    bio: Optional[str] = None
    books: list["BookResponseSchema"] = []

    class Config:
        from_attributes = True


class AuthorListSchema(BaseModel):
    id: int
    name: str
    books: Optional[list["BookResponseSchema"]]

    class Config:
        from_attributes = True


class BookCreateSchema(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: date

    class Config:
        from_attributes = True


class BookResponseSchema(BaseModel):
    id: int
    title: str
    summary: Optional[str] = None
    publication_date: date
    author_id: int

    class Config:
        from_attributes = True

