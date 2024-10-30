from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session, skip: int, limit: int):
    return (
        db.query(models.DBAuthor).offset
        (offset=skip).limit(limit=limit).all()
    )


def get_author_by_name(db: Session, name: str):
    return (
        db.query(models.DBAuthor).filter
        (models.DBAuthor.name == name).first()
    )


def get_author_by_id(db: Session, author_id: int):
    return (
        db.query(models.DBAuthor).filter
        (models.DBAuthor.id == author_id).first()
    )



def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_books(
        db: Session,
        skip: int,
        limit: int,
        author_id: int | None = None
):
    queryset = db.query(models.DBBook)

    if author_id:
        queryset = queryset.filter(models.DBBook.author.has(id=author_id))

    return queryset.offset(offset=skip).limit(limit=limit).all()


def get_book_by_id(db: Session, book_id: int):
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()


def book_create(db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
