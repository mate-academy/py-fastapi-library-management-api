from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class DBBook(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    summary = Column(String(255))
    publication_date = Column(DateTime)
    author_id = Column(Integer, ForeignKey("authors.id"))


class DBAuthor(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    bio = Column(String(255))
    books = relationship(DBBook)
