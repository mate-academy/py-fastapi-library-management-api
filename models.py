from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    bio = Column(String)

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    summary = Column(String)
    publication_date = Column(Date, nullable=False)

    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False) #actual database connection
    author = relationship("Author", back_populates="books") #sqlalchemy way to navigate that connection
