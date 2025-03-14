from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class AuthorModel(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True)
    bio = Column(String(500))
    books = relationship("BookModel")


class BookModel(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150))
    summary = Column(String(350))
    publication_data = Column(Date)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship("AuthorModel")
