from database import Base
from sqlalchemy import String, ForeignKey, Integer, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date

class DBAuthor(Base):
    __tablename__ = "author_model"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    bio: Mapped[str] = mapped_column(String(250))
    books: Mapped[list["DBBook"]] = relationship(back_populates="author")


class DBBook(Base):
    __tablename__ = "books_model"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    summary: Mapped[str] = mapped_column(String(200))
    publication_date: Mapped[date] = mapped_column(Date())
    author_id: Mapped[int] = mapped_column(ForeignKey("author_model.id"))
    author: Mapped["DBAuthor"] = relationship(back_populates="books")