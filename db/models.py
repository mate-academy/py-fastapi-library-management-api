from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from db.database import Base


class DBBook(Base):
    __tablename__: str = "Books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=True)
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("Authors.id"), nullable=False)


class DBAuthor(Base):
    __tablename__: str = "Authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    bio = Column(String, nullable=True)
    books = relationship(DBBook)



