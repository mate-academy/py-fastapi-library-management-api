from pydantic import BaseModel
from datetime import datetime


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime


class BookCreate(BookBase):
    author_id: int


class BookRead(BookBase):
    id: int
    author_id: int

    model_config = {
        "from_attributes": True
    }


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorRead(AuthorBase):
    id: int

    model_config = {
        "from_attributes": True
    }
