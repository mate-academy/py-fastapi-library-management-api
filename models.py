from datetime import date
from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship # type: ignore
from database import Base


class DBAutor(Base):
    __tablename__ = "autor"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    bio: Mapped[str] = mapped_column(String(511), nullable=False)
    books : Mapped[list["DBBook"]] = relationship("DBBook",back_populates="autor")

class DBBook(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    summary: Mapped[str] = mapped_column(String(511), nullable=False)
    publication_date: Mapped[date] = mapped_column(Date, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("autor.id"))
    autor: Mapped["DBAutor"] = relationship("DBAutor", back_populates="books")

