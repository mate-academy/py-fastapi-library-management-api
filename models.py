from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(123), nullable=False, unique=True)
    bio = Column(String(511), nullable=False)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    bio = Column(String(511), nullable=False)
    publication_date = Column(DateTime, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"))

    authors = relationship(Author)
