from sqlalchemy.orm import Session
from db import models
import schemas


def get_all_books(
    db: Session,
    author_id: int | None = None,
    skip: int = 0,
    limit: int = 10,
) -> list[models.Book]:
    queryset = db.query(models.Book)

    if author_id:
        queryset = queryset.filter(models.Book.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()


def get_book_by_id(db: Session, book_id: int) -> models.Book:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_all_authors(db: Session):
    return db.query(models.Author).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_by_id(db: Session, author_id: int):
    return (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )
