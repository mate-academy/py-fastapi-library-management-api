from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

import models
import schemas


def get_all_authors(
    db: Session,
    skip: int = 0,
    limit: int = 10,
) -> list[models.Author]:
    return (db.query(models.Author)
            .offset(skip)
            .limit(limit)
            .all())


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    try:
        db.commit()
        db.refresh(db_author)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Author with this name already exists"
        )
    return db_author


def get_author_by_name(db: Session, name: str) -> models.Author:
    return (
        db.query(models.Author).filter(models.Author.name == name).first()
    )


def get_author(db: Session, author_id: int) -> models.Author:
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_all_books(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: int = None
) -> list[models.Book]:
    queryset = db.query(models.Book).options(joinedload(models.Book.author))

    if author_id is not None:
        queryset = queryset.filter(
            models.Book.author_id == author_id
        )

    return queryset.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    try:
        db.commit()
        db.refresh(db_book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Error when adding new book into DB"
        )
    return db_book
