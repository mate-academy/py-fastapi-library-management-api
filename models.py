from sqlalchemy import Column, Integer, String, Date, ForeignKey, select
from sqlalchemy.orm import relationship, Mapped, mapped_column, column_property

from database import Base


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    bio = Column(String(512))
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(512))
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("author.id"))
    author = relationship(Author)
