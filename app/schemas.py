from datetime import date
from typing import Optional

from pydantic import BaseModel


class BookCreateSchema(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int

    model_config = {"from_attributes": True}


class BookDetailSchema(BaseModel):
    id: int
    title: str
    summary: str
    publication_date: date
    author_id: int

    model_config = {"from_attributes": True}


class BookUpdateSchema(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    publication_date: Optional[date] = None
    author_id: Optional[int] = None

    model_config = {"from_attributes": True}


class AuthorCreateSchema(BaseModel):
    name: str
    bio: str

    model_config = {"from_attributes": True}


class AuthorDetailSchema(BaseModel):
    id: int
    name: str
    bio: str
    books: Optional[list["BookDetailSchema"]] = None

    model_config = {"from_attributes": True}


class AuthorUpdateSchema(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None

    model_config = {"from_attributes": True}


class AuthorCreateResponseSchema(BaseModel):
    id: int
    name: str
    bio: str

    model_config = {"from_attributes": True}
