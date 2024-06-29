from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    bio = Column(String(255))


class DBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    summary = Column(String(255))
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship(DBAuthor)
#
#
# from sqlalchemy import Column, Integer, String, Date, ForeignKey
# from sqlalchemy.orm import relationship
#
# from database import Base
#
#
# class Author(Base):
#     __tablename__ = "author"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255), nullable=False, unique=True)
#     bio = Column(String(511))
#     books = relationship("Book", back_populates="author")
#
#
# class Book(Base):
#     __tablename__ = "book"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(255), nullable=False)
#     summary = Column(String(255), nullable=False)
#     publication_date = Column(Date, nullable=False)
#     author_id = Column(Integer, ForeignKey("author.id"), nullable=False)
#
#     author = relationship("Author", back_populates="books")
