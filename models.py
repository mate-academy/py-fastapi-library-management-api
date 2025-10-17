from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class AuthorModel(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    bio = Column(String, nullable=True)

    books = relationship("BookModel", back_populates="author")


class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=True)
    publication_date = Column(Date, nullable=True)

    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("AuthorModel", back_populates="books")
