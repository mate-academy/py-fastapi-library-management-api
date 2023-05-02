from sqlalchemy import Integer, Column, String, Date, ForeignKey

from sqlalchemy.orm import relationship

from library.database import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    bio = Column(String(500))
    books = relationship("DBBook", backref="author", lazy=True)


class DBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    summary = Column(String(500))
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)
