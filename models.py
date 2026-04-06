from datetime import date
from typing import List

from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    bio: Mapped[str] = mapped_column(String(255))
    books: Mapped[List["Book"]] = relationship(back_populates="author")


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(String(255))
    publication_date: Mapped[date] = mapped_column(Date)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)
    author: Mapped["Author"] = relationship(back_populates="books")
