from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(63), unique=True)
    bio: Mapped[str] = mapped_column()
    books: Mapped[list["Book"]] = relationship(
        back_populates="author", cascade="all, delete"
    )


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(63))
    summary: Mapped[str] = mapped_column()
    publication_date: Mapped[date] = mapped_column()
    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id", ondelete="CASCADE")
    )
    author: Mapped["Author"] = relationship(back_populates="books")
