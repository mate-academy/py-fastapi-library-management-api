from datetime import date

from sqlalchemy import ForeignKey, String, Date
from sqlalchemy.orm import Mapped, relationship, mapped_column

from db.database import Base


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    bio: Mapped[str] = mapped_column(String)
    books: Mapped[list["Book"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
    )


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
    summary: Mapped[str] = mapped_column(String)
    publication_date: Mapped[date] = mapped_column(Date)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped[Author] = relationship("Author", back_populates="books")
