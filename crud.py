from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author_by_name(db: Session, name: str):
    return (
        db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()
    )


def get_author_by_id(db: Session, authors_id: int):
    return (
        db.query(models.DBAuthor).filter(models.DBAuthor.id == authors_id).first()
    )


def create_author(db: Session, author: schemas.AuthorCreate):
    db_authors = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_authors)
    db.commit()
    db.refresh(db_authors)

    return db_authors


def get_book_list(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    author_id: int = None,
):
    if author_id is not None:
        return db.query(models.DBBook).filter(
            models.DBBook.author_id == author_id
        ).offset(skip).limit(limit).all()

    return db.query(models.DBBook).offset(skip).limit(limit).all()

def get_book(db: Session, book_id: int):
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
