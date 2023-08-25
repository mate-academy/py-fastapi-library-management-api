from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str | None = None
    publication_date: str
    author_id: int


class BookCreate(BookBase):
    title: str
    summary: str | None = None
    publication_date: str
    author_id: int


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    bio: str


class Author(AuthorBase):
    id: int
    books: list[Book] = []

    class Config:
        orm_mode = True
