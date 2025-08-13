from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database.engine import Base


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True, unique=True)
    bio = Column(String(511), nullable=True)


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=True)
    summary = Column(String(511), nullable=True)
    publication_date = Column(DateTime(timezone=True), nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'))

    author = relationship('Author', backref='books')
