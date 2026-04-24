from datetime import date

from sqlalchemy import ForeignKey, Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Author(Base):
    __tablename__ = 'author'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    bio: Mapped[str] = mapped_column(String(255))
    books: Mapped[list["Book"]] = relationship(back_populates="author", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = 'book'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(String(255))
    publication_date: Mapped[date] = mapped_column(Date, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"), nullable=False)
    author: Mapped[Author] = relationship(back_populates="books")
