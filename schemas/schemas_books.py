from pydantic import BaseModel
from datetime import date


class BaseBooks(BaseModel):
    title: str
    summary: str
    publication_date: date


class CreateBooks(BaseBooks):
    author_id: int


class GetBooks(BaseBooks):
    id: int
    author_id: int

    class Config:
        from_attributes = True