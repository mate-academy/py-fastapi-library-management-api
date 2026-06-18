from datetime import date
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    bio: Mapped[str] = mapped_column(String(511))
    books: Mapped[list["Book"]] = relationship(back_populates="author")


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(String(511))
    publication_date: Mapped[date]
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))

    author: Mapped[Author] = relationship(back_populates="books")
