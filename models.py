from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import BaseClass


class Author(BaseClass):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String(155),
        unique=True,
    )
    bio = Column(String(500))
    books = relationship("Book", back_populates="author")


class Book(BaseClass):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(155), nullable=False)
    summary = Column(String(1000), nullable=False)
    publication_date = Column(Date(), nullable=False)
    author_id = Column(
        ForeignKey("authors.id"),
    )

    author = relationship("Author", back_populates="books")
