from datetime import date

from sqlalchemy import Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    bio: Mapped[str] = mapped_column(Text)
    books: Mapped[list["Book"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(Text)
    publication_date: Mapped[date] = mapped_column(Date)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("authors.id"))

    author: Mapped[Author] = relationship(back_populates="books")
