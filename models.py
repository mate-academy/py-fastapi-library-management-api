from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    summary = Column(String(510), nullable=False)
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("authors.id"))


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True, nullable=False)
    bio = Column(String(510), nullable=False)
    books = relationship(Book)
