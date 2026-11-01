from sqlalchemy.orm import Session

import models
import schemas


def get_author(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def get_all_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books(db: Session, skip: int = 0, limit: int = 100, author_id: int | None = None):
    query = db.query(models.DBBook)
    if author_id is not None:
        query = query.filter(models.DBBook.author_id == author_id)
    return query.offset(skip).limit(limit).all()


def create_author_book(db: Session, book: schemas.BookCreate, author_id: int):
    # Исключаем author_id из словаря схемы, если он там был, чтобы избежать конфликта при распаковке
    book_data = book.model_dump(exclude={"author_id"})
    db_book = models.DBBook(**book_data, author_id=author_id)

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book