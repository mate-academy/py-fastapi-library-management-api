from sqlalchemy.orm import Session

import models
import schemas


def create_author(database: Session, author: schemas.AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    database.add(db_author)
    database.commit()
    database.refresh(db_author)
    return db_author


def get_all_authors(database: Session, skip: int = 0, limit: int = 10):
    return database.query(models.Author).offset(skip).limit(limit).all()


def get_author_by_id(database: Session, author_id: int):
    return database.query(models.Author).filter(models.Author.id == author_id).first()


def get_author_by_name(database: Session, author_name: str):
    return database.query(models.Author).filter(models.Author.name == author_name).first()


def create_book(database: Session, book: schemas.BookCreate):
    db_book = models.Author(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    database.add(db_book)
    database.commit()
    database.refresh(db_book)
    return db_book


def get_all_books(database: Session, skip: int = 0, limit: int = 10):
    return database.query(models.Book).offset(skip).limit(limit).all()


def get_book_by_author_id(database: Session, author_id: int | None = None, skip: int = 0, limit: int = 10):
    queryset = database.query(models.Book)

    if author_id is not None:
        queryset = queryset.filter(models.Book.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()
