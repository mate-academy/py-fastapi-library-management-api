from sqlalchemy import Column, Integer, String, DATE, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from db.database import Base


class DBBook(Base):
    __table_name__: str = "Books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    summary = Column(String)
    publication_date = Column(DATE)
    # author_id = Column(Integer, ForeignKey("Authors.id"))


class DBAuthor(Base):
    __table_name__: str = "Authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    bio = Column(String)
    # books = relationship(DBBook)



