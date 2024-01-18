from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    bio = Column(String)

    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return self.name


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True, nullable=False)
    summary = Column(String)
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship("Author", back_populates="books")

    def __repr__(self):
        return f"'{self.title}' by {self.author}"
