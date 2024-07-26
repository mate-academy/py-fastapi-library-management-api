from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from database import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    bio = Column(String(511))
    books = relationship("DBBook")


class DBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(255))
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship(DBAuthor, back_populates="books", overlaps="books")
