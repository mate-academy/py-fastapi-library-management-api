from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    bio = Column(String, nullable=False)

    books = relationship('Book', back_populates='author', cascade='all, delete-orphan')


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, nullable=False)
    summary = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'), nullable=False)

    author = relationship('Author', back_populates='books')
