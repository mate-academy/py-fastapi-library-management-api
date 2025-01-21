from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, orm

from database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), unique=True, nullable=False, index=True)
    summary = Column(String(256), unique=False, nullable=False)
    publication_date = Column(DateTime, unique=False, nullable=False)
    author_id = Column(ForeignKey("authors.id"))

    author = orm.relationship("Author", back_populates="books")


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    bio = Column(String(1000), nullable=True, unique=False)
    books = orm.relationship("Book", back_populates="author")
