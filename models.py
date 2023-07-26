from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class DBBook(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    summary = Column(String)
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    author = relationship('DBAuthor', back_populates="books")


class DBAuthor(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    bio = Column(String)
    books = relationship("Book", back_populates="author")
