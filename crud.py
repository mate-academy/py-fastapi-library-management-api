from fastapi import HTTPException, Depends, Query
from sqlalchemy.orm import Session

import models, schemas
from database import get_db


def get_books(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_authors(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int):
    book = db.query(models.Book).filter_by(id=book_id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


def get_author(db: Session, author_id: int):
    author = db.query(models.Author).filter_by(id=author_id).first()

    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


def create_book(db: Session, book: schemas.BookCreate):
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


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def update_book(db: Session, book_id: int, updated_book: schemas.BookCreate):
    db_book = get_book(db=db, book_id=book_id)

    db_book.title = updated_book.title
    db_book.author_id = updated_book.author_id
    db_book.summary = updated_book.summary
    db_book.publication_date = updated_book.publication_date

    db.commit()
    db.refresh(db_book)

    return db_book


def update_author(db: Session, author_id: int, updated_author: schemas.AuthorCreate):
    db_author = get_author(db=db, author_id=author_id)

    db_author.bio = updated_author.bio
    db_author.name = updated_author.name

    db.commit()
    db.refresh(db_author)

    return db_author


def delete_book(db: Session, book_id: int):
    db_book = get_book(db=db, book_id=book_id)

    db.delete(db_book)
    db.commit()

    return {"detail": f"Book with id {book_id} has been deleted"}


def delete_author(db: Session, author_id: int):
    db_author = get_author(db=db, author_id=author_id)

    db.delete(db_author)
    db.commit()

    return {"detail": f"Author with id {author_id} has been deleted"}
