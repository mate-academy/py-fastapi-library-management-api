from datetime import date

from db.database import Base
from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class DBAuthor(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=False)
    books: Mapped[list["DBBook"]] = relationship(back_populates="author")


class DBBook(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    publication_date: Mapped[date] = mapped_column(nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"), nullable=False)
    author: Mapped["DBAuthor"] = relationship(back_populates="books")

