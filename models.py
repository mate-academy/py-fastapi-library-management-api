from datetime import date

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    bio: Mapped[str]
    books: Mapped[list["Book"]] = relationship(back_populates="author")


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str]
    publication_date: Mapped[date]
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))

    author: Mapped["Author"] = relationship(back_populates="books")
