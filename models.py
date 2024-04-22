from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    bio = Column(String(1024))
    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return f"<Author(id={self.id}, name={self.name}, bio={self.bio})>"


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    summary = Column(String(255))
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship("Author", back_populates="books")
