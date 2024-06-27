from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: str


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str
    bio: str


class Author(AuthorBase):
    id: int
    books: list[Book] = []

    class Config:
        orm_mode = True
