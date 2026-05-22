from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Author(Base):
    __tablename__ = "authors" 

    id =  Column(Integer, primary_key=True, nullable=False)
    name =  Column(String(255), nullable=False)
    bio = Column(String(511), nullable=False)

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books" 

    id =  Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    summary = Column(String(511), nullable=False)
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    author = relationship("Author", back_populates="books")
