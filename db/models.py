from datetime import date

from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.engine import Base


class DBAuthor(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    bio: Mapped[str] = mapped_column(Text)
    books: Mapped[list["DBBook"]] = relationship(back_populates="authors")


class DBBook(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), unique=True)
    summary: Mapped[str] = mapped_column(Text)
    publication_date: Mapped[date] = mapped_column(server_default=func.current_date())
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))
    authors: Mapped["DBAuthor"] = relationship(back_populates="books")
