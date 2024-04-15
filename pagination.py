from datetime import date

from pydantic import BaseModel


class BookOut(BaseModel):
    id: int
    title: str
    summary: str
    publication_date: date
    author_id: int

    class Config:
        from_attributes = True


class AuthorOut(BaseModel):
    id: int
    name: str
    bio: str

    class Config:
        from_attributes = True
