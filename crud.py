from sqlalchemy.orm import Session
from sqlalchemy import select
import schemas
import models


def get_author_list(
    db: Session,
    skip: int = 0,
    limit: int = 10,
):
    stmt = select(models.Author).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def get_author_detail(db: Session, author_id: int):
    return db.scalar(select(models.Author).where(models.Author.id == author_id))


def create_author(db: Session, author: schemas.AuthorCreate):
    author_db = models.Author(name=author.name, bio=author.bio)
    db.add(author_db)
    db.commit()
    db.refresh(author_db)
    return author_db


def get_book_list(
    db: Session, skip: int = 0, limit: int = 10, author_ids: list[int] | None = None
):
    stmt = select(models.Book).offset(skip).limit(limit)
    if author_ids:
        stmt = stmt.where(models.Book.author_id.in_(author_ids))
    return db.scalars(stmt).all()


def create_book(db: Session, book: schemas.BookCreate):
    book_db = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(book_db)
    db.commit()
    db.refresh(book_db)
    return book_db
