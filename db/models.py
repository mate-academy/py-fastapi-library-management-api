from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship

from db.engine import Base


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    bio = Column(Text)


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, unique=True)
    summary = Column(String(255))
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship(Author)
