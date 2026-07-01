from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, relationship


class BaseModel(DeclarativeBase):
    __abstract__ = True
    id = Column(Integer, primary_key=True)


class AuthorsModel(BaseModel):
    __tablename__ = 'authors'

    name = Column(String, unique=True)
    bio = Column(String)
    books = relationship("BooksModel", back_populates="author")


class BooksModel(BaseModel):
    __tablename__ = 'books'

    title = Column(String)
    summary = Column(String)
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship("AuthorsModel", back_populates="books")
