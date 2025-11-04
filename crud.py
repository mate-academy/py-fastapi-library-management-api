from sqlalchemy import select
from sqlalchemy.orm import Session
import models
from schemas import CreateAuthorRequest, CreateBookRequest


def create_author(author: CreateAuthorRequest, db: Session):
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_authors(skip: int, limit: int, db: Session):
    stmt = select(models.Author).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def get_author(id: int, db: Session):
    stmt = select(models.Author).where(models.Author.id == id)
    return db.execute(stmt).scalars().first()


def create_book(book: CreateBookRequest, db: Session):

    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(skip: int, limit: int, author_id: int | None, db: Session):
    if author_id:
        stmt = (
            select(models.Book)
            .where(models.Book.author_id == author_id)
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()
    else:
        stmt = select(models.Book).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()


def get_book(id: int, db: Session):
    stmt = select(models.Book).where(models.Book.id == id)
    return db.execute(stmt).scalars().first()
