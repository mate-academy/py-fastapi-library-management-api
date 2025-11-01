from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), unique=True, nullable=False)
    bio = Column(String(512))
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    summary = Column(String(256))
    publication_date = Column(DateTime)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    author = relationship(Author, back_populates="books")
