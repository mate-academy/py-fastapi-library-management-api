from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    bio = Column(String(1000), nullable=False)
    books = relationship('Book', back_populates='authors')


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(1000), nullable=True)
    publication_date = Column(DateTime)
    author_id = Column(Integer, ForeignKey("author.id"))

    authors = relationship("Author", back_populates="books")
