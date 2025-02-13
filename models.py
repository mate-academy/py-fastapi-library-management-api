from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class DBAuthor(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    bio = Column(String(1024), nullable=True)
    books = relationship("DBBook", back_populates="author")

class DBBook(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(1024), nullable=True)
    publication_date = Column(Date, nullable=True)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship("DBAuthor", back_populates="books")

