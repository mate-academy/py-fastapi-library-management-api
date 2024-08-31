from database import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey
)
from sqlalchemy.orm import relationship


class Book(BaseModel):
    __tablename__ = "books"
    id = Column(
        Integer, primary_key=True, index=True
    )
    title = Column(
        String(255), nullable=False
    )
    summary = Column(String(255))
    publication_date = Column(Date)
    author_id = Column(
        Integer, ForeignKey("authors.id")
    )


class Author(BaseModel):
    __tablename__ = "authors"
    id = Column(
        Integer, primary_key=True, index=True
    )
    name = Column(
        String(255), unique=True, nullable=False
    )
    bio = Column(String(255))

    books = relationship(Book)
