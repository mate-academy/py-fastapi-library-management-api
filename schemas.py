from datetime import date
from pydantic import BaseModel, constr, computed_field
from typing import List, Optional


class BookCreateSchema(BaseModel):
    title: constr(max_length=255)
    summary: Optional[constr(max_length=2000)] = None
    publication_date: Optional[date] = None
    author_id: int


class BookReadSchema(BaseModel):
    id: int
    title: str
    summary: Optional[str] = None
    publication_date: Optional[date] = None
    author_id: int

    class Config:
        from_attributes = True


class AuthorCreateSchema(BaseModel):
    name: constr(max_length=255)
    bio: Optional[constr(max_length=1000)] = None


class AuthorReadSchema(BaseModel):
    id: int
    name: str
    bio: Optional[str] = None
    books: List[BookReadSchema] = []

    @computed_field
    @property
    def book_count(self) -> int:
        return len(self.books)

    class Config:
        from_attributes = True
