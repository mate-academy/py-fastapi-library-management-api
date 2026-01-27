from datetime import date
from typing import Optional, List

from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    bio: Mapped[Optional[str]]

    books: Mapped[List["Book"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[Optional[str]]
    publication_date: Mapped[Optional[date]] = mapped_column(Date)

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id", ondelete="CASCADE")
    )
    author: Mapped["Author"] = relationship(back_populates="books")
