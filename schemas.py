from datetime import date
from pydantic import BaseModel


class AuthorAddDTO(BaseModel):
    name: str
    bio: str


class AuthorPatchDTO(BaseModel):
    name: str | None = None
    bio: str | None = None



class AuthorDTO(AuthorAddDTO):
    id: int


class AuthorRelDTO(AuthorDTO):
    books: list["BookDTO"]


class BookAddDTO(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int


class BookDTO(BookAddDTO):
    id: int


class BookRelDTO(BookDTO):
    author: "AuthorDTO"
