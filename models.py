from database import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    bio = Column(String(500))
    books = relationship("Book", backref="author")


class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    summary = Column(String(500))
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey('authors.id'))
