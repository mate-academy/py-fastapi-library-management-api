from datetime import date

from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, relationship, mapped_column

from database import Base

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )
    summary: Mapped[str] = mapped_column(String(300), nullable=False)
    publication_date: Mapped[date] = mapped_column(
        default=date.today
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["Author"] = relationship(back_populates="books")


class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    bio: Mapped[str] = mapped_column(String(50))
    books: Mapped[list["Book"]] = relationship(back_populates="author")
