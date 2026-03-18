from sqlalchemy.orm import Session

import models
import schemas


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_authors(db: Session, skip=0, limit=100):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_one_author(db: Session, author_id: int):
    return db.get(models.Author, author_id)


def create_book_for_author(db: Session, author_id: int, book: schemas.BookCreate):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_all_books(db: Session, skip=0, limit=100, author_id=None):
    query = db.query(models.Book)

    if author_id is not None:
        query = query.filter(models.Book.author_id == author_id)

    return query.offset(skip).limit(limit).all()