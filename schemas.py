from datetime import date
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: Optional[date] = None


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)

class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int
    books: List[BookRead] = []
    model_config = ConfigDict(from_attributes=True)


