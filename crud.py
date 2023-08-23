from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session, skip: int, limit: int):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_books(db: Session, skip: int, limit: int, author_id: int):
    books = db.query(models.Book)

    if author_id is not None:
        books = books.filter(models.Book.author_id == author_id)

    return books.offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def create_book(db: Session, book: schemas.BookCreate):
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
