from sqlalchemy.orm import Session, joinedload

import models
import schemas


def get_all_authors(db: Session, limit: int, skip: int):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def get_author_by_name(db: Session, author_name: str):
    return db.query(models.DBAuthor).filter(models.DBAuthor.name == author_name).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_books(db: Session, limit: int, skip: int, author_id: int | None = None):
    queryset = db.query(models.DBBook).options(joinedload(models.DBBook.author))

    if author_id:
        queryset = queryset.filter(models.DBBook.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
