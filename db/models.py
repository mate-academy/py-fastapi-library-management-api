from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base

class Author(Base):
    __tablename__ = "author"

    id = Column(Integer(), primary_key=True, index=True)
    name = Column(String(255), unique=True)
    bio = Column(Text())

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer(), primary_key=True, index=True)
    title = Column(String(255))
    summary = Column(String(511))
    publication_date = Column(Date())
    author_id = Column(Integer(), ForeignKey("author.id"))

    author = relationship("Author", back_populates="books")