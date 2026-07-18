from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    Date,
    ForeignKey
)
from sqlalchemy.orm import relationship, ONETOMANY

from database import Base


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(Text(1025), nullable=False)
    publication_date = Column(Date, nullable=False)
    author_id = Column(
        ForeignKey("author.id", ondelete="CASCADE"),
        nullable=False
    )


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    bio = Column(Text(1025), nullable=False)
    books = relationship(Book)
