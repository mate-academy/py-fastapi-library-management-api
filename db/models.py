from sqlalchemy import Column, Integer, ForeignKey, Date, String
from sqlalchemy.orm import relationship

from db.database import Base


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    bio = Column(String(500))
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    summary = Column(String)
    publication = Column(Date)
    author_id = Column(Integer, ForeignKey("author.id"))
