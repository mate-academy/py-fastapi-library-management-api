from database import Base
from sqlalchemy import Column, String, Integer, relationship


class Author(Base):
    __tablename__ = "Author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    bio = Column(String(255), nullable=False)
    books = Column(String(255), nullable=False)
    

class Book(Base):
    __tablename__ = "Books"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    summary = Column(String(255))
    publication_date = Column(date)
    author_id = Column(foreign_key)
