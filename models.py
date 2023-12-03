from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Date


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(500), nullable=False)
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("author.id"))


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    biography = Column(String(500))

    books = relationship(Book, back_populates="author")
