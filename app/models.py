from sqlalchemy.orm import relationship

from app.database import Base
from sqlalchemy import Column, String, Integer, Date, ForeignKey


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(63), unique=True, index=True)
    bio = Column(String(1000))

    books = relationship("Book")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), index=True)
    summary = Column(String(1000))
    publication_date = Column(Date())
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("Author", back_populates="books")
