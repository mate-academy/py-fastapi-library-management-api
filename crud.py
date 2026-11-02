from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session, skip: int = 0, limit: int = 100) -> list[models.Author]:
    return db.scalars(select(models.Author).offset(skip).limit(limit)).all()


def get_author(db: Session, author_id: int):
    return db.scalar(
        select(models.Author).where(models.Author.id == author_id)
    )


def create_author(db: Session, author: schemas.AuthorCreate):
    author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def get_all_books(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        author_id: int | None = None
) -> list[models.Book]:
    books = select(models.Book)
    if author_id:
        books = books.where(models.Book.author_id == author_id)
    books = books.offset(skip).limit(limit)
    return list(db.scalars(books).all())


def create_book(
        db: Session,
        book: schemas.BookCreate,
        author_id: int | None = None
) -> models.Book:
    book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book
