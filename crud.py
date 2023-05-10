from sqlalchemy.orm import Session

import models
import schemas
from models import Author
from models import Book


def get_all_authors(db: Session, skip: int = 0, limit: int = 10) -> list[Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.Author) -> Author:
    db_author = Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_detail_author(db: Session, author_id: int) -> Author:
    return (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )


def update_author(db: Session, author_id: int, author: schemas.AuthorUpdate) -> Author | None:
    author_to_update = get_detail_author(db, author_id)
    if not author_to_update:
        return None
    for key, value in author.dict().items():
        setattr(author_to_update, key, value)
    db.commit()
    db.refresh(author_to_update)
    return author_to_update


def delete_author(db: Session, author_id: int) -> Author | None:
    author_to_delete = get_detail_author(db, author_id)
    if not author_to_delete:
        return None
    db.delete(author_to_delete)
    db.commit()
    return author_to_delete


def get_all_books(
        db: Session,
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 10
) -> Book:
    queryset = db.query(models.Book)

    if author_id is not None:
        queryset = queryset.filter(
            models.Book.author_id == author_id
        )

    return queryset.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate) -> Book:
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
