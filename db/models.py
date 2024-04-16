from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.engine import Base


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False, unique=True)
    bio = Column(String(511), nullable=False)
    books = relationship("Book", back_populates="author")

    def __repr__(self) -> str:
        return str(self.name)


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), nullable=False)
    summary = Column(String(512), nullable=False)
    publication_date = Column(DateTime)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")

    def __repr__(self) -> str:
        return str(self.title)
