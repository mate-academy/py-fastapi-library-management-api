from datetime import date
from typing import List, Optional

from sqlmodel import Field, SQLModel, Relationship


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, unique=True)
    summary: str | None
    publication_date: date | None
    author_id: int = Field(default=None, foreign_key="author.id")

    author: Optional["Author"] = Relationship(back_populates="books")


class Author(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    bio: Optional[str] = None

    books: list["Book"] = Relationship(back_populates="author")

Book.model_rebuild()
Author.model_rebuild()
