from datetime import date

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date

from database import Base


class DBAuthor(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    bio: Mapped[str] = mapped_column(String(511))
    books: Mapped[list["DBBook"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
    )


class DBBook(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(64))
    summary: Mapped[str] = mapped_column(String(511))
    publication_date: Mapped[date] = mapped_column(Date)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["DBAuthor"] = relationship(back_populates="books")
