import datetime
from tkinter.constants import CASCADE

from sqlalchemy import String, Text, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = declarative_base()


class AuthorModel(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    bio: Mapped[str] = mapped_column(Text, nullable=False)
    books: Mapped[list["BookModel"]] = relationship(
        "BookModel",
        back_populates="author"
    )

    @classmethod
    def default_order_by(cls):
        return [cls.id.desc()]


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    publication_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey(
        "authors.id",
        ondelete="CASCADE"),
        nullable=False
    )
    author: Mapped["AuthorModel"] = relationship("AuthorModel", back_populates="books")

    @classmethod
    def default_order_by(cls):
        return [cls.id.desc()]
