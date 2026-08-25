from datetime import date

from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from database import Base


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    bio: Mapped[str] = mapped_column(String(511), nullable=False)
    books: Mapped[list["Book"]] = relationship(back_populates="author")


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(String(255), nullable=False)
    publication_date: Mapped[date] = mapped_column(Date, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("author.id"))

    author: Mapped["Author"] = relationship(back_populates="books")
