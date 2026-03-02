from sqlalchemy.orm import Session

import models
import schemas


def get_authors(db: Session, skip: int = 0, limit: int = 100) -> list[models.DBAuthor]:
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.DBAuthor:
    db_author = models.DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author(db: Session, author_id: int, author_name: str = None) -> models.DBAuthor | None:
    if author_name:
        return db.query(models.DBAuthor).filter(models.DBAuthor.name == author_name).first()
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def create_book_for_author(
    db: Session, author_id: int, book: schemas.BookCreate
) -> models.DBBook:
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(
    db: Session, skip: int = 0, limit: int = 100, author_id: int | None = None
) -> list[models.DBBook]:
    query = db.query(models.DBBook)
    if author_id is not None:
        query = query.filter(models.DBBook.author_id == author_id)
    return query.offset(skip).limit(limit).all()
