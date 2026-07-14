from database import Base
from sqlalchemy import Column, String, Integer, relationship


class Author(Base):
    __tablename__ = "Author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    books = Column(String(255), nullable=False)
    
