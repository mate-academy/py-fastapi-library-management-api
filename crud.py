from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int):
    return (db.query(models.Author)
            .filter(models.Author.id == author_id)
            .first())


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_books(db: Session, skip: int = 0, limit: int = 100):
    return (db.query(models.Book)
            .offset(skip).limit(limit)
            .all())


def get_book_by_id(db: Session, book_id: int):
    return (db.query(models.Book)
            .filter(models.Book.id == book_id)
            .first())


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


def get_books_by_author_id(db: Session, author_id: int):
    return (
        db.query(models.Book)
        .filter(models.Book.author_id == author_id)
        .all()
    )


def get_author_by_name(db: Session, name: str):
    return (db.query(models.Author)
            .filter(models.Author.name == name)
            .first())


def create_book_for_author(db: Session, book: schemas.BookCreate, author_id: int):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
