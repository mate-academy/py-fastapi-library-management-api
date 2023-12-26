from sqlalchemy. orm import Session
import models
import schemas


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(db: Session, db_author: models.DBAuthor, author: schemas.AuthorUpdate):
    for attr, value in vars(author).items():
        setattr(db_author, attr, value) if value is not None else None

    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_by_id(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def get_paginated_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_paginated_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.DBBook).offset(skip).limit(limit).all()


def get_books_by_author_id(db: Session, author_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.DBBook).filter(models.DBBook.author_id == author_id).offset(skip).limit(limit).all()
