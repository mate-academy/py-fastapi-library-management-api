from pydantic import BaseModel
from typing import List
from typing import Optional
from datetime import date

class Book(BaseModel):
    id: int
    title: str
    summary: str
    publication_date: date

    class Config:
        orm_mode = True

class BookCreate(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int


class BookUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    publication_date: Optional[date] = None
    author_id: Optional[int] = None


class AuthorBase(BaseModel):
    name: str
    bio: str

    class Config:
        orm_mode = True

class Author(AuthorBase):
    id: int
    books: List[Book] = []

    class Config:
        orm_mode = True



class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass
