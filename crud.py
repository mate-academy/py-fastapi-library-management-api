from sqlalchemy.orm import Session

import models
from schemas import AuthorCreate, BookCreate


def get_all_authors(db: Session, skip: int, limit: int):
    return db.query(models.Author).slice(skip, limit)


def get_author_by_name(db: Session, name: str):
    return (
        db.query(models.Author).filter(models.Author.name == name).first()
    )


def get_author_by_id(db: Session, author_id: int):
    return (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )


def create_author(db: Session, author: AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_books_list(
        db: Session,
        skip: int,
        limit: int,
        author_id: int | None = None,
):
    queryset = db.query(models.Book)

    if author_id:
        queryset = queryset.filter(models.Book.author_id == author_id)

    return queryset.slice(skip, limit)


def create_book(db: Session, book: BookCreate):
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
