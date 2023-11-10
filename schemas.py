from datetime import date

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int

    @classmethod
    def from_attributes(cls, obj):
        return cls(**obj.__dict__)


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list[Book] = []

    @classmethod
    def from_attributes(cls, obj):
        author_dict = obj.__dict__
        author_dict["books"] = [
            Book.from_attributes(book) for book in author_dict.get("books", [])
        ]
        return cls(**author_dict)
