from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class DBBaseModel(Base):
    __abstract__ = True
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, index=True)


class DBBook(DBBaseModel):
    __tablename__ = "book"

    title = Column(String(255))
    summary = Column(String)
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("author.id"))
    author = relationship("DBAuthor", back_populates="books")


class DBAuthor(DBBaseModel):
    __tablename__ = "author"

    name = Column(String(50), unique=True)
    bio = Column(String(255))
    books = relationship(DBBook, back_populates="author")
