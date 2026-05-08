from typing import List

from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    bio: Mapped[str] = mapped_column(String(255))
    books: Mapped[List["DBBook"]] = relationship("DBBook")


class DBBook(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(unique=True)
    summary: Mapped[str] = mapped_column(String(255))
    publication_date: Mapped[Date] = mapped_column(Date)

    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped["DBAuthor"] = relationship("DBAuthor")
