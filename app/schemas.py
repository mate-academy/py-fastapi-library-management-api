from typing import List, Optional

from pydantic import BaseModel, PastDate, field_validator
from app.schema_validators.validators import StrLengthValidator


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: PastDate
    author_id: int

    @classmethod
    @field_validator("title")
    def title_length(cls, title: str) -> str:
        StrLengthValidator.validate("Book title", title, 255)

        return title


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str
    bio: str

    @classmethod
    @field_validator("name")
    def name_length(cls, name: str) -> str:
        StrLengthValidator.validate("Author name", name, 50)

        return name

    @classmethod
    @field_validator("bio")
    def bio_length(cls, bio: str) -> str:
        StrLengthValidator.validate("Author bio", bio, 255)

        return bio


class AuthorCreate(AuthorBase):
    books: Optional[List[BookCreate]] = []


class Author(AuthorBase):
    books: Optional[List[Book]] = []
