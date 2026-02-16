from __future__ import annotations

from datetime import date
from pydantic import BaseModel, ConfigDict


class AuthorDto(BaseModel):
    id: int | None = None
    name: str
    bio: str
    
    model_config = ConfigDict(from_attributes=True)


class AuthorCreateUpdateDto(BaseModel):
    name: str
    bio: str
    
    model_config = ConfigDict(from_attributes=True)


class AuthorDetailDto(AuthorDto):
    books: list["BookDto"] | None = None


class BookDto(BaseModel):
    id: int | None = None
    title: str
    summary: str
    publication_date: date

    author_id: int
    
    model_config = ConfigDict(from_attributes=True)


class BookCreateUpdateDto(BaseModel):
    title: str
    summary: str
    publication_date: date

    author_id: int
    
    model_config = ConfigDict(from_attributes=True)


class BookDetailDto(BookDto):
    author: AuthorDto
