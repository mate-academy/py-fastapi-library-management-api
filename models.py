import datetime

from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = "author"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    bio: Mapped[str]

    books: Mapped[List["Book"]] = relationship(
        back_populates="author", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str]
    publication_date: Mapped[datetime.datetime]
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))

    author: Mapped["Author"] = relationship(back_populates="books")

    def __repr__(self) -> str:
        return f"Book(id={self.id!r}, title={self.title!r}, author={self.id!r})"
