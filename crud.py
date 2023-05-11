from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session, offset: int = 0, limit: int = 10) -> None:
    return db.query(models.Author).offset(offset).limit(limit).all()


def get_author_by_name(db: Session, name: str) -> None:
    return (
        db.query(models.Author).filter(models.Author.name == name).first()
    )


def get_author_by_id(db: Session, authors_id: int) -> None:
    return (
        db.query(models.Author).filter(models.Author.id == authors_id).first()
    )


def create_author(db: Session, author: schemas.AuthorCreate) -> schemas.Author:
    db_authors = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_authors)
    db.commit()
    db.refresh(db_authors)

    return db_authors


def get_book_list(
    db: Session,
    offset: int = 0,
    limit: int = 10,
    author_id: int = None,
) -> None:
    if author_id is not None:
        return db.query(models.Book).filter(
            models.Book.author_id == author_id
        ).offset(offset).limit(limit).all()

    return db.query(models.Book).offset(offset).limit(limit).all()

def get_book(db: Session, book_id: int) -> None:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate) -> schemas.Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
