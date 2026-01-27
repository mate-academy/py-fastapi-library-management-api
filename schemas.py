from datetime import datetime
from typing import List

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str
    books: List["BookRead"] = []

    class Config:
        model_config = {
            "from_attributes": True
        }


class BookBase(BaseModel):
    id: int
    title: str
    summary: str
    publication_date: datetime

    class Config:
        model_config = {
            "from_attributes": True
        }


class BookRead(BookBase):
    pass

class AuthorRead(AuthorBase):
    id: int

class AuthorCreate(AuthorBase):
    pass
