from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from db.database import Base


class Book(Base):
    __tablename__ = "library_book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(127), nullable=False, unique=True)
    summary = Column(String(255), nullable=False)
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("library_author.id"))


class Author(Base):
    __tablename__ = "library_author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(127), nullable=False)
    bio = Column(String(511), nullable=False)
    books = relationship(Book)
