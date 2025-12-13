import datetime

from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .engine import Base


class Author(Base):
    __tablename__ = "author"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(63), unique=True)
    bio: Mapped[str] = mapped_column(String(511))
    book: Mapped[list["Book"]] = relationship(back_populates="author")


class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(63))
    summary: Mapped[str] = mapped_column(String(511))
    publication_date: Mapped[datetime.date] = mapped_column(Date)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped[Author] = relationship(back_populates="book")
