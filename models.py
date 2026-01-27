from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    bio = Column(Text, nullable=True)

    books = relationship(
        "Book",
        back_populates="author",
        cascade="all, delete-orphan",
    )


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    summary = Column(Text, nullable=True)
    publication_date = Column(Date, nullable=False)

    author_id = Column(Integer, ForeignKey("authors.id"),
                       nullable=False,
                       index=True)
    author = relationship("Author", back_populates="books")
    
