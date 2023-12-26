from sqlalchemy import (Column,
                        Integer,
                        String,
                        ForeignKey,
                        Date)
from database import Base


class DBAuthor(Base):
    __tablename__ = "Author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    bio = Column(String(500))


class DBBook(Base):
    __tablename__ = "Book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    summary = Column(String(500))
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("Author.id"))
