from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    bio = Column(String)

    books = relationship("Book", backref="author")


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    summary = Column(String)
    publication_date = Column(DateTime)
    author_id = Column(Integer, ForeignKey('author.id'))

    author = relationship(Author)
