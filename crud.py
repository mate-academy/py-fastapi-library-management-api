from sqlalchemy import select
from sqlalchemy.orm import Session

from models import AuthorModel, BookModel
from schemas import AuthorCreate, BookCreate


def get_author(db: Session, author_id: int) -> AuthorModel:
    return db.get(AuthorModel, author_id)

def get_author_by_name(db:Session, name: str) -> AuthorModel:
    stmt = select(AuthorModel).where(AuthorModel.name == name)
    return db.scalar(stmt)

def get_author(db: Session, skip: int = 0, limit: int = 10) -> list[AuthorModel]:
    stmt = select(AuthorModel).offset(skip).limit(limit)

def create_author(db: Session, author: AuthorCreate) -> AuthorModel:
    db_author = AuthorModel(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None,
) -> list[BookModel]:
    stmt = select(BookModel)
    if author_id is not None:
        stmt = stmt.where(BookModel.author_id == author_id)
    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def create_book(db: Session, book: BookCreate, author_id: int) -> BookModel:
    db_book = BookModel(**book.model_dump(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
