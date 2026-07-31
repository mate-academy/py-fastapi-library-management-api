from enum import StrEnum, auto

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.orm.dependency import OneToManyDP

from db.database import Base

class CoverType(StrEnum):
    SOFT = auto()
    HARD = auto()

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, index=True)
    summary = Column(String(511), nullable=False, index=True)
    publication_date = Column(Date, nullable=False, index=True)

    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    author = relationship("Author", back_populates="books")

    cover_type = Column(Enum(CoverType), nullable=False)


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True, unique=True)
    bio = Column(String(255), nullable=False, index=True)

    books = relationship("Book", back_populates="author")
