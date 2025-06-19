from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class DB_Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    bio = Column(String(512))

    books = relationship("DB_Book", back_populates="author")


class DB_Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    summary = Column(String(512))
    publication_date = Column(Date)

    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship("DB_Author", back_populates="books")
