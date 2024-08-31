from database import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(63), unique=True)
    bio = Column(String(255))
    books = relationship("Book")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(83))
    summary = Column(String(255))
    publication_date = Column(Date)
    author_id = Column(ForeignKey("author.id"))
    author = relationship("Author", back_populates="books")
