from datetime import date
from typing import Optional

from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from database import Base


class DBAuthor(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    bio: Mapped[Optional[str]] = mapped_column(String(510))
    books: Mapped[list["DBBook"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )


class DBBook(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(String(255))
    publication_date: Mapped[date] = mapped_column(Date, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["DBAuthor"] = relationship(back_populates="books")
