from pydentic import BaseModel

from typing import List, Optional

from datetime import date

class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: date

class BookCreate(BookBase):
    pass

class BookList(BookBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorList(AuthorBase):
    id: int
    books: List[BookList] = []

    class Config:
        from_attributes = True