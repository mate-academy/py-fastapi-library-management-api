from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field, ConfigDict


class BookCreate(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: Optional[date] = None
    author_id: int


class AuthorCreate(BaseModel):
    name: str
    bio: Optional[str] = None


class BookRead(BaseModel):
    id: int
    title: str
    summary: Optional[str] = None
    publication_date: Optional[date] = None
    author_id: int
    model_config = ConfigDict(from_attributes=True)


class AuthorRead(BaseModel):
    id: int
    name: str
    bio: Optional[str] = None
    books: List[BookRead] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)

