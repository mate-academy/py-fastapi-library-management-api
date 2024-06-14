from enum import StrEnum, auto

from sqlalchemy.orm import relationship

from database import Base

from sqlalchemy import Column, Integer, String, Date, ForeignKey


class PackagingType(StrEnum):
    IN_PACKAGE = auto()
    WEIGHT = auto()


class DBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    summary = Column(String(255), unique=True)
    publication_date = Column(Date)


class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    bio = Column(String(255))
    book_id = Column(Integer, ForeignKey("book.id"))

    book = relationship(DBBook)

# - id (integer, primary key)
# - name (string, unique)
# - bio (string)
# - books (relationship with the 'Book' model, one-to-many)

# - id (integer, primary key)
# - title (string)
# - summary (string)
# - publication_date (date)
# - author_id (foreign key referencing 'Author' model)
