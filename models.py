from datetime import date
from typing import List

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    bio: Mapped[str] = mapped_column(String(500))
    books: Mapped[List["Book"]] = relationship("Book", back_populates="author")

    @hybrid_property
    def books_titles(self) -> List[str]:
        return [book.title for book in self.books]

    def __str__(self) -> str:
        return self.name


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(String(500))
    publication_date: Mapped[date]
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("author.id"))
    author: Mapped[Author] = relationship(Author, back_populates="books")

    def __str__(self) -> str:
        return self.title
