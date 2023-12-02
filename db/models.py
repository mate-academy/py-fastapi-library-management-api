from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from db.engine import Base


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(31), unique=True, nullable=False)
    bio = Column(String(255), nullable=False, default="")

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(31), nullable=False)
    summary = Column(String(255), nullable=False, default="")
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)

    author = relationship(Author, back_populates="books")