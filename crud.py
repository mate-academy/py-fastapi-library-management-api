from sqlalchemy.orm import Session

import schemas
import models


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author_name = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author_name)
    db.commit()
    db.refresh(db_author_name)
    return db_author_name


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int):
    return (
        db.query(models.Author)
        .filter(models.Author.id == author_id)
        .first()
    )


def create_book(db: Session, book: schemas.BookCreate):
    author = (
        db.query(models.Author)
        .filter(models.Author.id == book.author_id)
        .first()
    )

    if author is None:
        return None

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


def get_books(db: Session, skip: int = 0, limit: int = 100, author_id: int = None):
    query = db.query(models.Book)
    if author_id:
        query = query.filter(models.Book.author_id == author_id)
    return query.offset(skip).limit(limit).all()
