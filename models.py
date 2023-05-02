import datetime

from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey, Date
from sqlalchemy.orm import relationship

from database import Base

author_book_table = Table(
    "author_book",
    Base.metadata,
    Column("author_id", Integer, ForeignKey("authors.id")),
    Column("book_id", Integer, ForeignKey("books.id")),
)


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), unique=True)
    bio = Column(Text)
    books = relationship("Book", secondary=author_book_table, back_populates="authors")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=63))
    summary = Column(Text)
    publication_date = Column(
        Date, default=datetime.date.today(), onupdate=datetime.date.today()
    )
    authors = relationship(
        "Author", secondary=author_book_table, back_populates="books"
    )
