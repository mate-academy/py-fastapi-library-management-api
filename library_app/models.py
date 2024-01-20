from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from library_app.database import Base


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(125), unique=True, nullable=False)
    bio = Column(String(512), nullable=True)

    book = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, unique=True)
    summary = Column(String(255), nullable=True)
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("author.id"))
    author = relationship("Author", back_populates="book")
