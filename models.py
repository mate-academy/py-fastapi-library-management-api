from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer(), primary_key=True, index=True)
    name = Column(String(63), nullable=False, unique=True)
    bio = Column(String(511))

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer(), primary_key=True, index=True)
    title = Column(String(255), nullable=False, unique=True)
    summary = Column(String(511))
    publication_date = Column(Date())
    author_id = Column(Integer(), ForeignKey("authors.id"))

    author = relationship(Author, back_populates="books")
