from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload, selectinload

import models
import schemas


def create_new_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.model_dump())

    db.add(db_author)
    db.commit()

    db.refresh(db_author)
    return db_author


def get_author_list(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.Author).options(selectinload(models.Author.books)).offset(offset).limit(limit).all()


def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def create_new_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()

    db.refresh(db_book)
    return db_book

def get_book_list(db: Session, offset: int = 0, limit: int = 100, author_id: int = None):
    query = db.query(models.Book)
    if author_id:
        query = query.filter(models.Book.author_id == author_id)
    return query.offset(offset).limit(limit).all()
