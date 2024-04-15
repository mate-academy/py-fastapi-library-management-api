from sqlalchemy.orm import Session

import models, schemas


def get_author_by_id(db: Session, author_id: int):
    return (
        db.query(models.DBAuthor).
        filter(models.DBAuthor.id == author_id).
        first()
    )


def get_author_by_name(db: Session, name: str):
    return (
        db.query(models.DBAuthor).
        filter(models.DBAuthor.name == name).
        first()
    )


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books(
        db: Session,
        author_id: int = None,
        skip: int = 0,
        limit: int = 100
):
    if author_id:
        queryset = (
            db.query(models.DBBook).
            filter(models.DBBook.author_id == author_id).
            offset(skip).
            limit(limit)
        )
    else:
        queryset = db.query(models.DBBook).offset(skip).limit(limit)

    return queryset


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
