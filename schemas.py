from datetime import date
from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str | None
    publication_date: date | None


class BookCreate(BookBase):
    author_id: int


class BookResponse(BookBase):
    id: int
    author_id: int
    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorResponse(AuthorBase):
    id: int
    books: list[BookResponse] = []
    class Config:
        from_attributes = True
