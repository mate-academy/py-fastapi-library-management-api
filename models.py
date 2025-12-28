import datetime
from typing import List, Optional

from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class DBBook(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(String(511))
    publication_date: Mapped[datetime.date] = (
        mapped_column(Date(), nullable=True)
    )
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("author.id"))
    author: Mapped["DBAuthor"] = relationship()

    def __str__(self):
        return "book"


class DBAuthor(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    bio: Mapped[str] = mapped_column(nullable=True)
    books: Mapped[List[DBBook]] = relationship()
