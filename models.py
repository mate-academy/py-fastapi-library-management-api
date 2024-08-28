from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Date
)
from sqlalchemy.orm import relationship

from database.engine import Base


class Author(Base):
    __tablename__ = 'author'

    author_id = Column(Integer, primary_key=True)
    name = Column(String)
    bio = Column(String)
    books = relationship('Book', back_populates='author')


class Book(Base):
    __tablename__ = 'book'

    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    summary = Column(String)
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey('author.id'), nullable=False)
    author = relationship('Author', back_populates='books')
