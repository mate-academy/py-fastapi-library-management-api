from pydantic import BaseModel
from datetime import date


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookList(BookBase):
    pass


class BookFilter(BaseModel):
    author_id: int | None = None


class BookDetail(BookBase):
    author_id: int | None = None


class BookCreate(BookDetail):
    pass


class BookUpdate(BookDetail):
    pass


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorList(AuthorBase):
    pass


class AuthorDetail(AuthorBase):
    books: list[BookBase] | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorDetail):
    books: list[BookBase] | None = None
