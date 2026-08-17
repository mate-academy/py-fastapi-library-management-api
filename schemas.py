from datetime import date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict



class BookBase(BaseModel):
    title: str
    summary: Optional[str] | None = None
    publication_date:  Optional[date] | None = None


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorResponse(AuthorBase):
    id: int
    books: List[BookResponse] = []

    model_config = ConfigDict(from_attributes=True)


