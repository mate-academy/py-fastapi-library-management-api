from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.engine import Base


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    bio = Column(String)
    books = relationship('Book', backref='author', lazy=True)


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    summary = Column(String, nullable=True)
    publication_date = Column(Date, nullable=True)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
