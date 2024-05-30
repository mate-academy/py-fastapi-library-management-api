from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from database import Base


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    bio = Column(String(255))
    books = relationship('Book')


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(255))
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'), nullable=False)

    author = relationship(Author)
