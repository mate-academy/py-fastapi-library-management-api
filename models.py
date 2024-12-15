from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class DBAuthor(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    bio = Column(String(512), index=True)
    books = relationship('DBBook', back_populates='author')


class DBBook(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    summary = Column(String(512), index=True)
    publication_date = Column(Integer, index=True)
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship(DBAuthor, back_populates='books')