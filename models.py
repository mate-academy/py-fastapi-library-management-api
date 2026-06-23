from datetime import date
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class DBAuthor(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(
        primary_key=True, index=True
    )
    name: Mapped[str] = mapped_column(
        String(), unique=True, index=True
    )
    bio: Mapped[Optional[str]] = mapped_column(String)

    books: Mapped[List["DBBook"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"DBAuthor(id={self.id!r}, name={self.name!r})"


class DBBook(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    summary: Mapped[Optional[str]] = mapped_column(String)
    publication_date: Mapped[date] = mapped_column(Date)

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id", ondelete="CASCADE"), index=True
    )

    author: Mapped["DBAuthor"] = relationship(back_populates="books")

    def __repr__(self) -> str:
        return f"DBBook(id={self.id!r}, title={self.title!r})"
