import datetime
from typing import Optional, List

from sqlalchemy import (String,
                        Date,
                        ForeignKey)
from sqlalchemy.orm import Mapped, relationship, mapped_column

from db.database import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    bio: Mapped[Optional[str]] = mapped_column(String(1000))
    books: Mapped[List["DBBook"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )


class DBBook(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[Optional[str]] = mapped_column(String(2000))
    publication_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))

    author: Mapped["DBAuthor"] = relationship(
        back_populates="books"
    )
