from sqlalchemy import Integer, String, Column, ForeignKey, Date
from sqlalchemy.orm import relationship

from database import Base


class AuthorModel(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    bio = Column(String(512), nullable=True)
    
    books = relationship("BookModel", back_populates="author")


class BookModel(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), unique=True, nullable=False)
    summary = Column(String(512), nullable=True)
    published_date = Column(Date, nullable=True)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)

    author = relationship("AuthorModel", back_populates="books")
