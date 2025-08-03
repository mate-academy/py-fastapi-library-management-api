from sqlalchemy.orm import Session

import models
import schemas


# ----------------- Author block ---------------
def get_all_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def author_update(db: Session, author_id: int, author: schemas.AuthorUpdate):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not db_author:
        return None

    for key, value in author.model_dump().items():
        setattr(db_author, key, value)

    db.commit()
    db.refresh(db_author)
    return db_author


def author_delete(db: Session, author_id: int):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not db_author:
        return None
    db.delete(db_author)
    db.commit()
    return db_author


# ----------------- Book block ---------------
def get_all_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book_by_author_id(db: Session, author_id: int):
    return db.query(models.Book).filter(models.Book.author_id == author_id).all()


def book_create(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def book_update(db: Session, book_id: int, book: schemas.BookUpdate):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        return None

    for key, value in book.model_dump().items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book


def book_delete(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        return None
    db.delete(db_book)
    db.commit()
    return db_book
