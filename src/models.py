from sqlalchemy import ForeignKey, String
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Author(Base):
    __tablename__ = "author"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    bio: Mapped[str | None] = mapped_column(String(100))
    books: Mapped[list["Book"] | None] = relationship(back_populates="author")

    def __repr__(self):
        return f"<Author {self.name}>"


class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    summary: Mapped[str] = mapped_column(String(100))
    publication_date: Mapped[date] = mapped_column()
    author_id: Mapped[int | None] = mapped_column(ForeignKey("author.id"))
    author: Mapped["Author"] = relationship(back_populates="books")
