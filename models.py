from datetime import datetime
from typing import List
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class DBAuthor(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    bio: Mapped[str] = mapped_column(String())
    books: Mapped[List["DBBook"]] = relationship(
        back_populates="author", 
        cascade="all, delete-orphan"
    )


class DBBook(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(String()) 
    publication_date: Mapped[datetime] = mapped_column(server_default=func.now())
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))

    author: Mapped["DBAuthor"] = relationship(back_populates="books")
