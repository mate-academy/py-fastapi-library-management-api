from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(55), nullable=False)
    bio = Column(String(555), nullable=False)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(55), nullable=False)
    summary = Column(String(255), nullable=False)
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship(Author, backref="books")
