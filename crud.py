from sqlalchemy.orm import Session

import models
import schemas


def get_authors(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int):
    return (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )


def create_author(db: Session, author: schemas.AuthorCreate):
    author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def get_books(
        db: Session,
        skip: int = 0,
        limit: int = 50,
        author_id: int | None = None
):
    queryset = db.query(models.Book)

    if author_id is not None:
        queryset = queryset.filter(models.Book.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate):
    book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(book)
    db.commit()
    db.refresh(book)

    return book
