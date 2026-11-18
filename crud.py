from sqlalchemy.orm import Session
from sqlalchemy import select

import models
from schemas import AuthorCreate, BookCreate


def get_authors(db: Session, skip: int = 0, limit: int = 1):
    return db.scalars(select(models.Author).offset(skip).limit(limit)).all()


def get_author_id(db: Session, author_id: int):
    return db.scalar(select(models.Author).where(models.Author.id == author_id))


def get_author_name(db: Session, name: str):
    return db.scalar(select(models.Author).where(models.Author.name == name))


def create_author(db: Session, author: AuthorCreate):
    book_list = db.scalars(
        select(models.Book).where(models.Book.id.in_(author.book_ids))
    ).all()

    db_author = models.Author(
        name=author.name,
        bio=author.bio,
        books=book_list
    )

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author

def get_books(
        db: Session,
        skip: int = 0,
        limit: int = 1,
        author_id: int | None = None,
):

    stmt = select(models.Book)

    if author_id is not None:
        stmt = stmt.where(models.Book.author_id == author_id)
    stmt = stmt.order_by(models.Book.id).offset(skip).limit(limit)

    return db.scalars(stmt).all()


def get_book_title(db: Session, title: str):
    return db.scalar(select(models.Book).where(models.Book.title == title))


def get_book_id(db: Session, book_id: int):
    return db.scalar(select(models.Book).where(models.Book.id == book_id))


def create_book(db: Session, book: BookCreate):
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


