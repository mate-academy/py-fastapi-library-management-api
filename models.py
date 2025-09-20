from datetime import date

from sqlalchemy import Integer, String, ForeignKey, Date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from base import Base


class DbAuthor(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    bio: Mapped[str] = mapped_column(String(511), nullable=False)
    books: Mapped[list["DbBook"]] = relationship(back_populates="author")


class DbBook(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    summary: Mapped[str] = mapped_column(String(1000), nullable=False)
    publication_date: Mapped[date] = mapped_column(Date, nullable=False)
    author_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("authors.id", ondelete="CASCADE"),
        nullable=False
    )
    author: Mapped["DbAuthor"] = relationship(back_populates="books")
