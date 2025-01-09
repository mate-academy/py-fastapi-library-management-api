from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from database import Base


class Author(Base):
    __tablename__ = 'Author'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    bio = Column(String(255), nullable=False)


class Book(Base):
    __tablename__ = 'Book'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    summary = Column(String(255), nullable=False)
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("Author.id"))
    author = relationship("Author")
