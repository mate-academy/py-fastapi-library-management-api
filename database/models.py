from datetime import datetime, date
from typing import Optional

from sqlalchemy import Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


base = DeclarativeBase()

class AuthorModel(base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    bio: Mapped[str] = mapped_column(String)

    books: Mapped[list["BookModel"]] = relationship(
        argument="BookModel",
        back_populates="author"
    )

class BookModel(base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(String, nullable=True)
    publication_date: Mapped[date] = mapped_column(Date, default=datetime.now, nullable=True)

    author_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("authors.id", ondelete="CASCADE"),
        nullable=True,
    )

    author: Mapped[Optional["AuthorModel"]] = relationship(argument="AuthorModel", back_populates="books")
