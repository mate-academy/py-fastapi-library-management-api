from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from schemas import AuthorCreate, BookCreate


def get_all_authors(
        db: Session,
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
):
    queryset = select(models.Author)

    if author_id is not None:
        queryset = queryset.where(models.Author.id == author_id)

    return db.scalars(queryset.offset(skip).limit(limit)).all()


def get_author_by_id(db: Session, author_id: int) -> models.Author | None:
    return db.scalar(
        select(models.Author).where(models.Author.id == author_id)
    )

def get_author_by_name(db: Session, name: str):
    return (
        db.scalar(select(models.Author).where(models.Author.name == name))
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
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
):
    queryset = select(models.Book)

    if author_id is not None:
        queryset = queryset.where(
            models.Book.author_id == author_id
        )

    return db.scalars(queryset.offset(skip).limit(limit)).all()

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
