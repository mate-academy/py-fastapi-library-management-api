from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from database import Base


class DBAuthor(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(63), unique=True)
    bio = Column(String(511))

    books = relationship("DBBook", back_populates="author")


class DBBook(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(63), unique=True)
    summary = Column(String(255))
    published_date = Column(Date)
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("DBAuthor", back_populates="books")
