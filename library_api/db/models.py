from sqlalchemy import Integer, String, Column, Date, ForeignKey
from sqlalchemy.orm import relationship

from library_api.db.engine import Base


class DBAuthor(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    bio = Column(String(511), nullable=False)
    books = relationship("DBBook", backref="author_obj", lazy=True)

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name}"


class DBBook(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, unique=True)
    summary = Column(String(511), nullable=False)
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)
    author = relationship("DBAuthor", backref="book", lazy=True)

    def __repr__(self):
        return (
            f"Book(id={self.id}, title={self.title}, author_id"
            f"={self.author_id})"
        )
