from datetime import date
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"


class Author(Base):
    name: Mapped[str] = mapped_column(unique=True)
    bio: Mapped[str]
    books: Mapped[list["Book"]] = relationship(back_populates="author")
    # profiles: Mapped["Profile"] = relationship(back_populates="author")

    def __repr__(self) -> str:
        return self.name


class Book(Base):
    title: Mapped[str]
    summary: Mapped[str]
    publication_date: Mapped[date]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["Author"] = relationship(back_populates="books")

    def __repr__(self) -> str:
        return self.title


# example of one to one relationship
# class Profile(Base):
#     name: Mapped[str] = mapped_column(unique=True)
#     author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), unique=True)
#     author: Mapped["Author"] = relationship(back_populates="profile")
#
#     __table_args__ = (UniqueConstraint("author_id"),)  # unique constraint for author_id(one to one)
