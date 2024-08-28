from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List, Optional

import schemas
import models


def get_all_authors(
        db: Session, skip: int = 0, limit: int = 10
) -> List[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int) -> Optional[models.Author]:
    return db.query(models.Author).filter(
        models.Author.author_id == author_id
    ).first()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    try:
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail='Error creating author: Integrity constraint violated'
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=str(e)
        )
    return db_author


def get_all_books(
        db: Session, author_id: int, skip: int = 0, limit: int = 10
) -> List[models.Book]:
    queryset = db.query(models.Book)

    if author_id:
        queryset = queryset.filter(models.Book.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.book_id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    try:
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail='Error creating book: Integrity constraint violated'
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=str(e)
        )
    return db_book
