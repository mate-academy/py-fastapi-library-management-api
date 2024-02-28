from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class DBAuthor(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True, )
    name = Column(String(63), nullable=False, unique=True, )
    bio = Column(String)

    # Define the one-to-many relationship with Book
    books = relationship("Book", back_populates="author")


class DBBook(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(63), nullable=False, )
    summary = Column(String)
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey('authors.id'))

    # Define the many-to-one relationship with Author
    author = relationship("Author", back_populates="books")

