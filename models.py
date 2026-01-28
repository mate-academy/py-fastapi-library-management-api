from datetime import date

from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(63), nullable=False, unique=True)
    bio: Mapped[str] = mapped_column(String(511), nullable=False)
    books: Mapped[list["Book"]] = relationship(back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(63), nullable=False)
    summary: Mapped[str] = mapped_column(String(511), nullable=False)
    publication_date: Mapped[date] = mapped_column(Date, nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id"), index=True, nullable=False
    )
    author: Mapped["Author"] = relationship(back_populates="books")
