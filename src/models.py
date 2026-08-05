from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Author(Base):
    __tablename__ = "author"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    bio: Mapped[str | None] = mapped_column(String(100))
    books: Mapped[list["Book"] | None] = relationship(back_populates="author")

    def __repr__(self):
        return f"<Author {self.name}>"


class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    summary: Mapped[str] = mapped_column(String(100))
    publication_date: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now()
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped[list["Author"]] = relationship(back_populates="books")
