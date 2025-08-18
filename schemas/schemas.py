import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


# --- Base Models ---
class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date
    author_id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorBase(BaseModel):
    name: str
    bio: str

    model_config = ConfigDict(from_attributes=True)


# --- Requests ---
class BookCreateRequest(BookBase):
    pass


class AuthorCreateRequest(AuthorBase):
    pass


# --- Responses ---
class BookCreateResponse(BookBase):
    id: int


class AuthorCreateResponse(AuthorBase):
    id: int


class AuthorListResponse(BaseModel):
    authors: List[AuthorCreateResponse] = Field(default_factory=list)


class BookListResponse(BaseModel):
    books: Optional[List[BookCreateResponse]] = []
