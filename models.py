from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class DBAuthor(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    bio = Column(String)
    books = relationship("DBBook", back_populates="author")


class DBBook(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)
    summary = Column(String)
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("author.id"))
    author = relationship("DBAuthor", back_populates="books")
