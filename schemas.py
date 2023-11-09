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
    def from_orm(cls, obj):
        return cls.from_attributes(**obj.__dict__)


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


from pydantic import BaseModel


class Author(AuthorBase):
    id: int
    books: list[Book] = []

    @classmethod
    def from_orm(cls, obj):
        author_dict = obj.__dict__
        author_dict["books"] = [
            Book.from_orm(book) for book in author_dict.get("books", [])
        ]
        return cls.from_attributes(**author_dict)
