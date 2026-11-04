from __future__ import annotations
from sqlalchemy import String, ForeignKey, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from database import Base


class DBAuthor(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(250), unique=True)
    bio: Mapped[str] = mapped_column(String(511))
    books: Mapped[list[DBBook]] = relationship(back_populates="author")


class DBBook(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(String(255))
    publication_date: Mapped[datetime.date] = mapped_column(Date)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    author: Mapped[DBAuthor] = relationship(back_populates="books")
