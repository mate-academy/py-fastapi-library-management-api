from datetime import date
from typing import List

from sqlmodel import Field, SQLModel, Relationship


class Author(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=200, index=True)
    bio: str

    books: List["Book"] = Relationship(back_populates="author", cascade_delete=True)


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=255, index=True)
    summary: str = Field(max_length=200)
    publication_date: date
    author_id: int = Field(foreign_key="author.id")

    author: "Author" = Relationship(back_populates="books")
