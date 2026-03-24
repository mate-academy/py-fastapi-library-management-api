from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
import models
import schemas


def author_exists(
        db: Session,
        name: str = None,
        author_id: int = None
) -> bool:
    stmt = select(models.Author)
    if name is not None:
        stmt = stmt.where(models.Author.name == name)
    if author_id is not None:
        stmt = stmt.where(models.Author.id == author_id)
    return db.scalars(stmt).first() is not None


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    stmt = select(models.Author).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author(db: Session, author_id: int):
    stmt = select(models.Author).where(models.Author.id == author_id)
    return db.scalars(stmt).first()


def get_books(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None
):
    stmt = select(models.Book)

    if author_id:
        stmt = stmt.where(models.Book.author_id == author_id)

    stmt = stmt.options(joinedload(models.Book.author))
    stmt = stmt.offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
