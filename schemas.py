from datetime import date

from pydantic import BaseModel


class BookBase(BaseModel):
    name: str
    title: str
    summary: str
    publication_date: date
    author_id: int

    model_config = {"from_attributes": True}


class BookResponse(BookBase):
    id: int


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorResponse(AuthorBase):
    id: int
