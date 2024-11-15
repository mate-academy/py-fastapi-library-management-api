from sqlalchemy.orm import Session

import models
import schemas


def create_book(db: Session, book: schemas.BookSCHCreate):
    db_book = models.Book(
        title=book.title,
        author_id=book.author_id,
        publication_date=book.publication_date,
        summary=book.summary,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_all_books(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(models.Book)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_book_by_author_id(db: Session, author_id: int):
    return (
        db.query(models.Book)
        .filter(models.Book.author_id == author_id)
        .all()
    )


def create_author(db: Session, author: schemas.AuthorSCHCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_authors(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(models.Author)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_author_by_id(db: Session, author_id: int):

    return (
        db.query(models.Author)
        .filter(models.Author.id == author_id)
        .one_or_none()
    )
