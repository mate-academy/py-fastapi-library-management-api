from datetime import date
from typing import List

from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


class Book(Base):
    __tablename__ = "Books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(String(300))
    publication_date:  Mapped[date] = mapped_column(Date)
    author_id: Mapped[int] = mapped_column(ForeignKey("Authors.id"))
    author: Mapped["Author"] = relationship(back_populates="books")


class Author(Base):
    __tablename__ = "Authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    bio: Mapped[str] = mapped_column(String(500))
    books: Mapped[List[Book]] = relationship(back_populates="author", cascade="all, delete-orphan")
